from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import CustomAuthenticationForm, RegisterUserForm
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
