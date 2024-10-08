from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import UpdateView
from social_django.utils import psa

from .forms import (
    CustomAuthenticationForm,
    RegisterUserForm,
    ProfileUserForm,
    UserPasswordChangeForm
)

from cards.models import Card
from cards.views import MenuMixin


class LoginUser(MenuMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.GET.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class SocialAuthView(View):

    @psa('social:complete')
    def save_oauth_data(self, request, backend):
        user = request.user
        if backend.name == 'github':
            user.github_id = backend.get_user_id(request)
        elif backend.name == 'vk-oauth2':
            user.vk_id = backend.get_user_id(request)
        user.save()
        return redirect('users:profile')

    def post(self, request, *args, **kwargs):
        if 'provider' in request.POST:
            provider = request.POST['provider']
            if provider == 'github':
                return redirect('social:begin', backend='github')
            elif provider == 'vk-oauth2':
                return redirect('social:begin', backend='vk-oauth2')
        return redirect('users:profile')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')


class RegisterUser(MenuMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:register_done')


class RegisterDoneView(LoginRequiredMixin, MenuMixin, TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {'title': 'Регистрация завершена'}


class ProfileUser(LoginRequiredMixin, MenuMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя', 'active_tab': 'profile'}

    def get_success_url(self):
        # URL на которую будет перенаправлен пользователь после редактирования профиля
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # Возвращает объект пользователя для редактирования
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Смена пароля', 'active_tab': 'password_change'}
    success_url = reverse_lazy('users:password_change_done')


class UserPasswordChangeDone(PasswordChangeView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Смена пароля завершена'}


class UserCardsView(ListView):
    model = Card
    template_name = 'users/profile_cards.html'
    extra_context = {'title': 'Мои карточки', 'active_tab': 'profile_cards'}
    context_object_name = 'cards'

    def get_queryset(self):
        return Card.objects.filter(author=self.request.user).order_by('-upload_date')
