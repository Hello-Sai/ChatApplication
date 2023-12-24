from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self,'user'):
            if not self.name:
                self.name = self.user.username

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(Profile,related_name="messages",on_delete=models.SET)
    timestamp = models.DateTimeField(auto_now_add=True,editable=False)
    recepient = models.ForeignKey(Profile,on_delete = models.SET)
    message = models.TextField()
    
    class Meta:
        ordering =('timestamp',)

    def __str__(self) -> str:
        return f'{self.sender} - {self.recepient}  \t {self.message}'