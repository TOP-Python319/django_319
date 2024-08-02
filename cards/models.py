from django.db import models


class Card(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=5000)
    upload_date = models.DateTimeField(auto_now_add=True, db_column='upload_date')
    views = models.IntegerField(default=0)
    adds = models.IntegerField(default=0)

    class Meta:
        db_table = 'Cards'  # без указания этого параметра, таблица в БД будет называться вида 'cards_card'
        verbose_name = 'Карточка'  # единственное число для отображения в админке
        verbose_name_plural = 'Карточки'  # множественное число для отображения в админке

    def __str__(self):
        return f'Карточка "{self.question}" — {self.answer[:50]}'


"""
1. Модель - это класс, который наследуется от models.Model
2. Поля модели - это атрибуты класса, которые являются экземплярами классов Field
3. Вложенный класс Meta - это метаданные модели
4. db_table - это имя таблицы в базе данных
5. verbose_name - это имя модели в единственном числе
6. verbose_name_plural - это имя модели во множественном числе
"""

"""
### CRUD Операции с моделью Card

1. Добавление данных
```python
card = Card.objects.create(
    question='Python or perl?',
    answer='Python',
)
card.save()
```
```python
card = Card.objects.create(
    question='Python or ruby?',
    answer='Python',
)
card.save()
```
2. Чтение данных
```python
# get - получение данных, но только одной записи
card = Card.objects.get(id=1)
card = Card.objects.get(pk=1)  # pk отличается от id, тем что pk ссылается на первичный ключ (в таблице) вне зависимости от его названия
card = Card.objects.get(question='Python or ruby?')

card = Card.objects.get(answer='Python')  # если несколько записей, то выдаст ошибку
```
```python
# all - получение всех данных
cards = Card.objects.all()  # получение всех карточек в виде итерируемого объекта

for card in Card.objects.all():
    print(card.question)
```

3. Обновление данных
```python
card = Card.objects.get(pk=1)
card.question = 'Python or PHP?'
card.save()
```

4. Удаление данных
```python
card = Card.objects.get(pk=1)
card.delete()
```
"""
