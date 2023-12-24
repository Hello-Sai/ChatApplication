"""
ASGI config for ws project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from chat import routing
# from wsapp.consumers import *
from channels.routing import ProtocolTypeRouter,URLRouter
from chat.consumers import *
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ws.settings')

application = get_asgi_application()

# ws_patterns = [
#     path('test/',TestConsumer.as_asgi()),
#     path('new/',NewConsumer.as_asgi())
# ]
# "http": get_asgi_application(),     # For Http Connection
application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    'websocket':AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
})
