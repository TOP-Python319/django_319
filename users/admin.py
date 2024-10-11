from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    list_per_page = 10
    list_editable = ('is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'date_birth', 'photo')}),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('wide',),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('collapse',),
            'fields': ('username', 'password', 'email'),
        }),
    )