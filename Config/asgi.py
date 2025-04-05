import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from Messages import consumers  # مصرف‌کننده شما در برنامه 'Messages' است

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/chat/', consumers.ChatConsumer.as_asgi()),  # مسیر WebSocket
            ]
        )
    ),
})

#c