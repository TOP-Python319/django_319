from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from .forms import MessageForm
from .models import Message, User
from cards.views import MenuMixin


class ChatView(MenuMixin, LoginRequiredMixin, View):
    template_name = 'chat/chat.html'
    form_class = MessageForm

    def get(self, request, user_id=None):
        form = self.form_class()
        messages = self.get_messages(request, user_id)
        users = self.get_users(request)

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'messages': messages,
                'users': users,
                'current_user_id': user_id,
            }
        )

    def post(self, request, user_id=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            send_to_all = form.cleaned_data['send_to_all']
            self.handle_message(request, user_id, content, send_to_all)

            if user_id is not None:
                return redirect(reverse('chat', kwargs={'user_id': user_id}))
            else:
                return redirect('chat')

        messages = self.get_messages(request, user_id)
        users = self.get_users(request)

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'messages': messages,
                'users': users,
                'current_user_id': user_id,
            }
        )

    def get_messages(self, request, user_id):
        # получение списка сообщений админа
        if request.user.is_superuser:
            # сообщения конкретного пользователя
            if user_id:
                recipient = User.objects.get(id=user_id)
                messages = Message.objects.filter(
                    Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user) | Q(sender__is_superuser=True)
                ).order_by('-timestamp')
            else:
                # сообщения всех пользователей
                messages = Message.objects.all()
        # сообщения пользователя
        else:
            messages = Message.objects.filter(
                Q(sender=request.user) | Q(recipient=request.user, sender__is_superuser=True)
            ).order_by('-timestamp')
        return messages

    def get_users(self, request):
        return User.objects.filter(is_superuser=False) if request.user.is_superuser else None

    def handle_message(self, request, user_id, content, send_to_all):
        if request.user.is_superuser:
            if send_to_all:
                for user in User.objects.filter(is_superuser=False):
                    Message.objects.create(
                        sender=request.user,
                        recipient=user,
                        content=content
                    )
            else:
                recipient = User.objects.get(id=user_id)
                Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    content=content
                )
        else:
            for admin in User.objects.filter(is_superuser=True):
                Message.objects.create(
                    sender=request.user,
                    recipient=admin,
                    content=content
                )
