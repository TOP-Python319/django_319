from django.db import models
from users.models import User  # Импортируйте вашу кастомную модель пользователя


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'
