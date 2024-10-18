from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),  # For chat rooms
    re_path(r'ws/private/(?P<username>\w+)/$', consumers.PrivateChatConsumer.as_asgi()),  # For private chats
]
