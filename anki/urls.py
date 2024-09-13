"""
anki/urls.py
"""
from django.views.decorators.cache import cache_page

from django.contrib import admin
from django.urls import path, include
from anki import settings
from cards import views


admin.site.site_header = 'Административная панель проекта ANKI'  # текст в шапке админ. панели
admin.site.site_title = 'Управление карточками ANKI'  # текст в заголовке браузера или вкладки админ. панели
admin.site.index_title = 'Добро пожаловать!'  # текст на главной странице админ. панели


# Подключаем файл urls.py из приложения cards через include
urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Маршруты для меню
    path('', cache_page(60 * 15)(views.IndexView.as_view()), name='index'),
    path('about/', cache_page(60 * 15)(views.AboutView.as_view()), name='about'),
    # Маршруты подключенные из приложения cards
    path('cards/', include('cards.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
