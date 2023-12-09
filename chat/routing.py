from django.urls import path

from wsapp.consumers import TestConsumer
from .consumers import ChatConsumer
# ws_patterns = [
#     path('chat/',ChatConsumer.as_asgi())
# ]
websocket_urlpatterns = [
    path('chat/<room_name>',ChatConsumer.as_asgi()),
    path('',TestConsumer.as_asgi())
]
