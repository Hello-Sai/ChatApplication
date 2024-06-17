# from cgitb import text
import json
# from django.urls import path
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync

class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name='test_consumer'
        self.group_name = "test_consumer_group"
        (self.channel_layer.group_add)(
            "test_consumer_group",
            self.channel_name
        )
        self.accept()
        self.send(text_data = json.dumps({'status':"Hoooo! Connected"}))
    def receive(self,text_data):
        print(text_data)
        text_data=text_data.split(':')

        print(text_data)
        self.send(json.dumps({'status':'Yeah I have received','You Send':text_data if text_data else ""}))
    def disconnect(self):
        print('Disconnected')

    def send_notification(self,event):
        self.send(json.dumps({'data':json.loads(event['value'])}))
    def CountApp(self,data):
        self.send(json.dumps({'data':json.loads(data['value'])}))
class NewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'new_consumer'
        self.room_group_name='new_consumer_group'
        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data = json.dumps({'Wish':'Hi'}))
    async def receive(self):
        pass
    async def disconnect(self):
        pass
    async def CountApp(self,data):
        await self.send(json.dumps({'data':json.loads(data['value'])}))