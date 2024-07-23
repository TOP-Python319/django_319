from django.urls import path
from . import views
# cards/urls.py
# будет иметь префикс в urlах /cards/


urlpatterns = [
    path('', views.get_all_cards),
    path('<int:card_id>/', views.get_card_by_id),
]
