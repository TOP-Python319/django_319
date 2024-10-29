from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm


@login_required
def chat(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                user=request.user,
                content=form.cleaned_data['content']
            )
            return redirect('chat')
    else:
        form = MessageForm()

    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'chat/chat.html', {
        'form': form,
        'messages': messages
    })
