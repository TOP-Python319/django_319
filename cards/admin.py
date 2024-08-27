from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # поля, которые будут отображаться в админке
    list_display = ('question', 'category', 'views', 'upload_date')

    # поля, которые будут ссылками
    list_display_links = ('question', 'category',)

    # поля, которые будут включены в поиск
    search_fields = ('answer',)  # не забываем поставить запятую в конце, если у нас только одно значение, что показать Python, что это кортеж

    # поля, которые будут фильтроваться
    list_filter = ('category',)
