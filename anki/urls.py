"""
anki/urls.py
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

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
    # Маршруты подключенные из приложения users
    path('users/', include('users.urls', namespace='users')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# добавляем обработку медиафайлов
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# определяем кастомный обработчик 404 ошибки
handler404 = views.PageNotFoundView.as_view()
