from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from .forms import MessageForm
from users.models import User

@login_required
def chat(request, user_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            send_to_all = form.cleaned_data['send_to_all']
            if request.user.is_superuser:
                if send_to_all:
                    # Админ отправляет сообщение всем пользователям
                    for user in User.objects.filter(is_superuser=False):
                        Message.objects.create(sender=request.user, recipient=user, content=content)
                else:
                    # Админ отправляет сообщение текущему пользователю
                    recipient = User.objects.get(id=user_id)
                    Message.objects.create(sender=request.user, recipient=recipient, content=content)
                return redirect('chat', user_id=user_id)
            else:
                # Пользователь отправляет сообщение админу
                admin = User.objects.filter(is_superuser=True).first()
                Message.objects.create(sender=request.user, recipient=admin, content=content)
                return redirect('chat')
    else:
        form = MessageForm()

    if request.user.is_superuser:
        if user_id:
            # Админ видит чат с текущим пользователем
            recipient = User.objects.get(id=user_id)
            messages = Message.objects.filter(Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)).order_by('timestamp')
        else:
            # Админ видит все сообщения
            messages = Message.objects.all()
    else:
        # Пользователь видит свои сообщения и сообщения от админа
        messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user, sender__is_superuser=True)).order_by('timestamp')

    users = User.objects.filter(is_superuser=False) if request.user.is_superuser else None

    return render(request, 'chat/chat.html', {'form': form, 'messages': messages, 'users': users, 'current_user_id': user_id})
