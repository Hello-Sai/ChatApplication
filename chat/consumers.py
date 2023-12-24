from django.urls import path
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from chat.models import Message, Profile
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_id= self.scope['user'].id
        other_id= int(self.scope['url_route']['kwargs']['id'])
        self.user = self.scope['user']
        self.room_name = f'{my_id}-{other_id}' if my_id < other_id else f'{other_id}-{my_id}'
        self.group_name = f'chat_{self.room_name}'
        await(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data = json.dumps({'payload':'connected'}))
    async def receive(self,text_data):
        await(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_message',
                'value':text_data
            }
        )
    async def disconnect(self, code):
        await(self.channel_layer.group_discard)(
            self.group_name,self.channel_name
        )
        return await super().disconnect(code)
    async def send_message(self,text_data):
        data = json.loads(text_data['value'])
        await self.save_message(data)
        await self.send(text_data=json.dumps(data))
    @database_sync_to_async
    def save_message(self,data):
        profile = Profile.objects.get(id = data['recepient'])
        self.user.profile.messages.create(recepient=profile,message =data['message'])
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await (self.channel_layer.group_add)(
            "online",self.channel_name
        )
        self.user  = self.scope['user']
        await self.update_status(True)
        await self.accept()

        message = {'status':True,'id':self.user.profile.id}
        await (self.channel_layer.group_send)(
            "online",{
                'type':'status_online',
                "value":message
            }
        )
    async def receive(self, text_data):
        return await super().receive(text_data)
    
    async def disconnect(self, code):
        message = {'status':False,'id':self.user.profile.id}
        await (self.channel_layer.group_send)(
            "online",{
                'type':'status_online',
                "value":message
            }
        )
        await self.update_status(False)
        await(self.channel_layer.group_discard)(
            "online",self.channel_name
        )
        return await super().disconnect(code)
    @database_sync_to_async
    def update_status(self,status):
        self.user.profile.status = status
        self.user.profile.save()
    async def status_online(self,event):
        await self.send(text_data=json.dumps(event['value']))