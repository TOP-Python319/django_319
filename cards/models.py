from django.contrib.auth import get_user_model
from django.db import models


class Card(models.Model):
    class Status(models.IntegerChoices):
        UNCHECKED = 0, 'не проверно'
        CHECKED = 1, 'проверено'

    id = models.AutoField(primary_key=True, db_column='CardID')
    question = models.CharField(max_length=255, db_column='Question', verbose_name='Вопрос')
    answer = models.TextField(max_length=5000, db_column='Answer', verbose_name='Ответ')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, db_column='CategoryID', verbose_name='Категория')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='UploadDate', verbose_name='Дата загрузки')
    views = models.IntegerField(default=0, db_column='Views', verbose_name='Просмотры')
    adds = models.IntegerField(default=0, db_column='Favorites', verbose_name='Добавления в избранное')
    tags = models.ManyToManyField('Tag', through='CardTag', related_name='cards', verbose_name='Теги')
    status = models.BooleanField(default=0, choices=(map(lambda x: (bool(x[0]), x[1]), Status.choices)), verbose_name='Проверено')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None, verbose_name='Автор')

    class Meta:
        db_table = 'Cards'  # без указания этого параметра, таблица в БД будет называться вида 'cards_card'
        verbose_name = 'Карточка'  # единственное число для отображения в админке
        verbose_name_plural = 'Карточки'  # множественное число для отображения в админке

    def __str__(self):
        return f'Карточка "{self.question}" — {self.answer[:50]}'

    def get_absolute_url(self):
        return f'/cards/{self.id}/detail/'


class Tag(models.Model):
    id = models.AutoField(primary_key=True, db_column='TagID')
    name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тег "{self.name}"'


class CardTag(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_column='CardID')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='TagID')

    class Meta:
        db_table = 'CardTags'
        verbose_name = 'Тег карточки'
        verbose_name_plural = 'Теги карточек'

        # уникальные пары карточка-тег
        unique_together = ('card', 'tag')

    def __str__(self):
        return f'Тег карточки "{self.card.question}" — {self.tag.name}'


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='CategoryID')
    name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория "{self.name}"'



"""
1. Модель - это класс, который наследуется от models.Model
2. Поля модели - это атрибуты класса, которые являются экземплярами классов Field
3. Вложенный класс Meta - это метаданные модели
4. db_table - это имя таблицы в базе данных
5. verbose_name - это имя модели в единственном числе
6. verbose_name_plural - это имя модели во множественном числе
"""
