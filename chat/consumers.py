from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
# from asgiref.sync import sync_to_async
# from django.contrib.auth.models import User
from django.db.models import Q,Count
from chat.models import Message
from chat.serializers import ChatNotificationSerializer
@database_sync_to_async
def get_profile(profile_id):
    from chat.models import ChatNotification, Profile
    return Profile.objects.get(id=profile_id).user.id

def get_channel(my_id,other_id):
    return f'{my_id}-{other_id}' if my_id < other_id else f'{other_id}-{my_id}'
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_id= self.scope['user'].id
        other_id= int(self.scope['url_route']['kwargs']['id'])
        self.user = self.scope['user']
        self.room_name = get_channel(my_id,other_id)
        self.group_name = f'chat_{self.room_name}'
        await(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # await self.see_notifications()
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
        # profile = await get_profile(data["recepient"])
        # await get_channel_layer().group_send(f'{profile}',{
        #     'type':"send_individual_notification",
        #     "value":json.dumps({})
        #     })
        print('sended')
    @database_sync_to_async
    def save_message(self,data):
        from chat.models import ChatNotification, Profile
        sender_profile = Profile.objects.get(id = data['sender'])
        recepient_profile = Profile.objects.get(id = data['recepient'])
        message  = Message.objects.create(sender= sender_profile,recepient=recepient_profile,message =data['message'])
        print(message.sender,message.recepient)
        notification = ChatNotification.objects.create(user = recepient_profile,chat = message)
        print('sending')
        
    @database_sync_to_async
    def see_notifications(self):
        from chat.models import ChatNotification, Profile
        my_id = self.scope['user'].id
        profile = Profile.objects.get(user__id = my_id)
        ChatNotification.objects.filter(user = profile).update(is_seen=True)
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
        await self.update_status(False)
        await (self.channel_layer.group_send)(
            "online",{
                'type':'status_online',
                "value":message
            }
        )
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





class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id 
        self.user = self.scope['user']

        self.group_name =    f'{my_id}'    
        await (self.channel_layer.group_add)(
            f'{my_id}',self.channel_name
        )
        await (self.channel_layer.group_send)(
            f'{my_id}',{
            'type':'send_individual_notification_count'
        })
        
        # await self.see_notification()
        await self.accept()
        
        # await self.send("NOTIFICATION SOCKET CONNECTED")
    async def check_notifications(self,event):
        print('called')
        data = json.loads(event.get('value'))
        await self.see_notifications(data['id'])
    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        data = json.loads(text_data)
        # print(text_data)
        print("id",data['id'])
        await (self.channel_layer.group_send)(
            self.group_name,{
            'type':'check_notifications',
            "value":json.dumps(data)
        })
            
    async def disconnect(self, code):
        my_id = self.scope['user'].id        
        await (self.channel_layer.group_discard)(
            f'{my_id}',self.channel_name
        )
        await self.send("NOTIFICATION SOCKET DISCONNECTED")

    @database_sync_to_async
    def see_notifications(self,id):
        from chat.models import ChatNotification, Profile
        # objs = ChatNotification.objects.filter(user = self.scope['user'].profile.id,chat__sender__id = id,is_seen=False)
        objs = self.user.profile.chatnotification_set.filter(chat__sender__id = id,is_seen=False)
        # print(objs.values('user'),end="\t")
        objs.update(is_seen=True)
        
    

    
    # async def send_notification_count(self,event):
    #     my_id = self.scope['user'].id        
    #     profile = await sync_to_async(Profile.objects.get)(id = my_id)
    #     count = await sync_to_async(ChatNotification.objects.filter)(user = profile,is_seen=False)
    #     count = await sync_to_async(count.count)()
    #     print(count,'=count')
    #     await self.send(json.dumps({'count':count}))

    

    @database_sync_to_async
    def get_notifications(self,profile_id):
        from chat.models import ChatNotification, Profile,Message
        distinct_chat_ids = ChatNotification.objects.filter(
            user_id=profile_id, is_seen=False
        ).values_list('chat__sender__id', flat=True).distinct()
        # messages = Message.objects.filter(recepient__id = self.group_name).values('sender')
        # senders_message_count =list( Message.objects.filter(recepient__id=profile_id).values('sender').annotate(count=Count('id')))
        senders_message_count = list(
            ChatNotification.objects.filter(user__id = profile_id,chat__sender__id__in =distinct_chat_ids,is_seen=False ).values('chat__sender').annotate(count =Count('id'))
        )
        print(senders_message_count)
        return senders_message_count
        # print(messages.values_list('sender__id',flat=True))
        # distinct_ids = list(set(messages.values_list('sender__id',flat=True)))
        # print(distinct_ids)
        # notifications = []
        # notifications = self.user.profile.chatnotification_set.filter(chat__sender__id__in =distinct_ids,is_seen=False )
        # # notifications = ChatNotification.objects.filter(user__id=user_id,is_seen=False,chat__sender__id__in = distinct_ids)
        # print(notifications)
        # notifications = notifications.filter(chat__sender__id__in = exclude_ids,is_seen=False)
        # Retrieve ChatNotification objects based on distinct chat instances
        
        
        # notifications = ChatNotification.objects.filter(
        # chat_id__in=distinct_chat_ids, is_seen=False)
        # return notifications
    

    # @database_sync_to_async
    # def get_chatnotification_serializer(self,notifications):
    #     return ChatNotificationSerializer(notifications, many=True).data
    
    @database_sync_to_async
    def get_profile(self):
        return self.user.profile

    async def send_individual_notification_count(self, event):
        # my_id = self.group_name
        profile = await self.get_profile()
        # print(my_id)
        # profile = await self.get_profile(my_id)
        # print(profile)
        notifications = await self.get_notifications(profile.id)
        # serialized_data= await self.get_chatnotification_serializer(notifications)
        print(notifications)
        await self.send(json.dumps(notifications))