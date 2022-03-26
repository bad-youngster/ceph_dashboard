"""
ASGI config for dashboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# add webssh models
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .consumers import SSHConsumer
from django.urls import path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([path(r'ws/ssh/<str:ip>', SSHConsumer.as_asgi())]
                  )
    )
})
