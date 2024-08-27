from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # поля, которые будут отображаться в админке
    list_display = ('pk', 'question', 'category', 'views', 'upload_date', 'status', 'has_code')

    # поля, которые будут ссылками
    list_display_links = ('pk', 'category',)

    # поля, которые будут включены в поиск
    search_fields = ('answer',)  # не забываем поставить запятую в конце, если у нас только одно значение, что показать Python, что это кортеж

    # поля, по которым можно фильтровать
    list_filter = ('category', 'status',)

    # сортировка по умолчанию по какому полю и в каком направлении
    ordering = ('category', '-views',)

    # постраничная навигация (пагинация, пейджинация)
    list_per_page = 10

    # редактируемые поля (без проваливания в карточку)
    list_editable = ('question', 'views', 'status',)

    # действия с карточками
    actions = ('set_checked', 'set_unchecked')

    @admin.display(description='Наличие кода')
    def has_code(self, card):
        return 'Да' if '```' in card.answer else 'Нет'

    @admin.action(description='Отметить карточку как проверенную')
    def set_checked(self, request, queryset):
        updated = queryset.update(status=Card.Status.CHECKED)
        self.message_user(request, f'{updated} карточек было отмечено как проверенные')

    @admin.action(description='Отметить карточку как не проверенную')
    def set_unchecked(self, request, queryset):
        updated = queryset.update(status=Card.Status.UNCHECKED)
        self.message_user(request, f'{updated} карточек было отмечено как не проверенные')
