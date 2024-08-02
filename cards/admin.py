from django.contrib import admin
from .models import Card


class CardAdmin(admin.ModelAdmin):
    pass


admin.site.register(Card, CardAdmin)
