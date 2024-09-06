# cards/forms.py

import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Category


class CodeBlockValidator:

    def __call__(self, value):
        # проверяем, содержит ли поле `value` код
        if '```' not in value:
            return

        # ищем все блоки кода, которые заключены в ```
        code_blocks = re.findall(r'```[\s\S]+?```', value)

        if not code_blocks:
            raise ValidationError('Нет закрывающей пары ```')

        # проверяем каждый блок кода на соответсвие списку правил
        for code_block in code_blocks:
            self.validate_code_block(code_block)

    def validate_code_block(self, block):

        # находим индексы открывающих и закрывающих ```
        opening_tick_index = block.find('```')
        closing_tick_index = block.rfind('```')

        # если индексы совпадают, значит закрывающие ``` отсутсвуют
        if opening_tick_index == closing_tick_index:
            raise ValidationError('Нет закрывающей пары ```')

        # есть ли пробел перед открывающей ```
        if block[opening_tick_index - 1] == ' ':
            raise ValidationError('Уберите пробел перед открывающими ```')

        # ищем начало содерижмого после открывающих ```
        content_start = opening_tick_index + 3

        if block[content_start] == ' ':
            raise ValidationError('Уберите пробел после открывающих ```')

        # Ищем конец строки с названием языка программирования (первый перенос строки после ```)
        language_name_end = block.find('\n', content_start)
        # Проверяем, есть ли название языка и достаточно ли оно длинное
        if language_name_end == -1 or language_name_end - content_start < 2:
            raise ValidationError("Добавьте название языка программирования после открывающих ```")

        # Проверяем, есть ли перенос строки после названия языка
        if block[language_name_end + 1] != '\n':
            raise ValidationError("Проверьте, что нет пробелов перед открытием блока кода, и есть перенос строки после названия языка.")

        # Проверяем, нет ли пробелов перед закрывающими ```
        if block[closing_tick_index - 1] == ' ':
            raise ValidationError("Уберите пробел перед закрывающими ```")



class CardForm(forms.Form):
    question = forms.CharField(
        label='Вопрос',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    answer = forms.CharField(
        label='Ответ',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 40}),
        max_length=5000,
        validators=[CodeBlockValidator()]
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Категория не выбрана',
    )
