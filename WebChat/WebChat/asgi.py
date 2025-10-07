import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns
from chat.authSocket import JwtAuthSocketMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebChat.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JwtAuthSocketMiddleware(
            URLRouter(
                websocket_urlpatterns)
        ),
    }
)
