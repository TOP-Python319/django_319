from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # list_display = ('question', 'answer', 'upload_date', 'views', 'adds',)
    # list_filter = ('upload_date', 'views', 'adds',)
    # list_per_page = 10
    # search_fields = ('answer',)
    # fields = (('question', 'answer'), ('views', 'adds'))
    pass
