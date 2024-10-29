from django.db import models
from users.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', default=1)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient', default=1)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_broadcast = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} {self.content}'
