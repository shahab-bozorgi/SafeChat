from django.db import models

from Accounts.models import User


class Message(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.content[:20]}"