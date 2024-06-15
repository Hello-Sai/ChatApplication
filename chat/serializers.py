from rest_framework import serializers

class ChatNotificationSerializer(serializers.ModelSerializer):
    chat = serializers.SerializerMethodField()
    class Meta:
        from chat.models import ChatNotification

        model = ChatNotification
        fields = ('chat',)

    def get_chat(self,obj):
        from chat.models import ChatNotification
        
        chat_notifications = ChatNotification.objects.filter(chat__recepient__id=obj.chat.recepient.id,chat__sender__id = obj.chat.sender.id,is_seen=False).distinct()
        return {'count':chat_notifications.count(),'user_id':obj.chat.sender.id}