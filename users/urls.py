from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path, reverse_lazy
from . import views


app_name = 'users'

urlpatterns = [
    # Вход, выход, регистрация
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    # Сообщение об успешной регистрации
    path('register_done/', views.RegisterDoneView.as_view(), name='register_done'),
    # Профиль, изменение пароля, мои карточки
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password_change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password_change_done/', views.UserPasswordChangeDone.as_view(), name='password_change_done'),
    path('profile_cards/', views.UserCardsView.as_view(), name='profile_cards'),

    # маршрут для сброса пароля
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        success_url=reverse_lazy('users:password_reset_done'),
        email_template_name='users/password_reset_email.html',
    ), name='password_reset'),

    # маршрут для подтверждения сброса пароля
    path('password_reset_done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    # маршрут для ввода нового пароля
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    # маршрут для завершения сброса пароля
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
