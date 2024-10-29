from django.db import models
from users.models import User  # Импортируйте вашу кастомную модель пользователя


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', default=1)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', default=1)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_broadcast = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.username}: {self.content}'
