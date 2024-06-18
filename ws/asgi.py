"""
ASGI config for ws project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ws.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from chat import routing
from django.core.asgi import get_asgi_application
from django.urls import path
from chat import routing

# Ensure the environment variable is set before setting up Django

django_asgi_app = get_asgi_application()

# Define the application protocol router
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # For HTTP connections
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Your WebSocket routes
        )
    ),
})

app = application