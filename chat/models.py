# import json
# from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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
        return self.name+' '+str(self.id)


class Message(models.Model):
    sender = models.ForeignKey(Profile,related_name="messages",on_delete=models.SET)
    timestamp = models.DateTimeField(auto_now_add=True,editable=False)
    recepient = models.ForeignKey(Profile,on_delete = models.SET)
    message = models.TextField()
    class Meta:
        ordering =('timestamp',)

    def __str__(self) -> str:
        return f'{self.sender} - {self.recepient}  \t {self.message}'
    
class ChatNotification(models.Model):
    chat = models.ForeignKey(Message,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.chat.sender.name} - {self.user} '

@receiver(post_save,sender = ChatNotification)
def notify_user(sender,instance,created,**kwargs):
    if created:
        # unseen_messages = sender.objects.filter(user = instance.user,is_seen=False).count()
        channel_layer = get_channel_layer()
        user_id = str(instance.user.id)
        # data = {
        #     'count':unseen_messages
        # }
        async_to_sync(channel_layer.group_send)(
            user_id,
            {
                'type':'send_individual_notification_count',
                # 'value':'created'
            }
        )