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