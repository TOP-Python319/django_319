from django.urls import path
from . import views
# cards/urls.py
# будет иметь префикс в urlах /cards/


urlpatterns = [
    path('catalog/', views.catalog),
    path('catalog/<int:card_id>/', views.get_card_by_id),
    path('catalog/<slug:slug>/', views.get_category_by_name),
    path('', views.get_all_cards),
]
