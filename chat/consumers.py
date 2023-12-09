from django.urls import path
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'room_%s'%self.room_name
        await(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data = json.dumps({'payload':'connected'}))
    async def receive(self,text_data):
        data = json.loads(text_data) if text_data else {}
        payload = {'message':data.get('message'),'sender':data.get('sender')}
        await(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_message',
                'value':payload
            }
        )
        await self.send(text_data)
    async def disconnect(self, code):
        return await super().disconnect(code)
    async def send_message(self,text_data):
        data = text_data['value']
        await self.send(text_data=json.dumps({'payload':data}))