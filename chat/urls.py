from django.urls import path
from . import views


urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('<int:user_id>/', views.ChatView.as_view(), name='chat'),
]
