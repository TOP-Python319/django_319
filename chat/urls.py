from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat, name='chat'),
    path('<int:user_id>/', views.chat, name='chat'),
]
