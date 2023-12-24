from django.urls import path

from wsapp.consumers import TestConsumer
from .consumers import ChatConsumer,OnlineStatusConsumer
# ws_patterns = [
#     path('chat/',ChatConsumer.as_asgi())
# ]
websocket_urlpatterns = [
    path('chat/<id>',ChatConsumer.as_asgi()),
    path('chats/online',OnlineStatusConsumer.as_asgi())
    # path('',TestConsumer.as_asgi()),
    # path('chats/<number>',AsyncChatConsumer.as_asgi())
]
