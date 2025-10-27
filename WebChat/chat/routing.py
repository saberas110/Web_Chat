from django.urls import re_path
from . import consumers

websocket_urlpatterns = [

    re_path(r'^ws/presence/$', consumers.PresenceConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<conversation_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/user/(?P<other_user_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]