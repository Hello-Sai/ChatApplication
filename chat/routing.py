from django.urls import path

from chat.consumers import ChatConsumer, NotificationConsumer,OnlineStatusConsumer
# ws_patterns = [
#     path('chat/',ChatConsumer.as_asgi())
# ]
websocket_urlpatterns = [
    path('chat/<id>',ChatConsumer.as_asgi()),
    path('chats/online',OnlineStatusConsumer.as_asgi()),
    path('chats/notifications',NotificationConsumer.as_asgi())
    # path('',TestConsumer.as_asgi()),
    # path('chats/<number>',AsyncChatConsumer.as_asgi())
]
