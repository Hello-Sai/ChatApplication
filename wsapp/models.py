from django.db import models
from django.contrib.auth.models import User
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notification =models.TextField(max_length=100)
    is_seen = models.BooleanField(default=False)


    def save(self,*args,**kwargs):
        channel_layer = get_channel_layer()
        data  = {'user':self.user.username,'notification':self.notification,'Is Seen':self.is_seen}
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group',
            {
                'type':'send_notification',
                'value':json.dumps(data) ,
                'value1':'Hello'
            }
        )
        super(Notification,self).save(*args,**kwargs)