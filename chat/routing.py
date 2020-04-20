from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/chat/$', consumers.AsyncChatConsumer),
    re_path(r'^ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]