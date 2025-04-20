# stt_pos/routing/websocket.py
from django.urls import re_path
from . import consumers  # This will refer to your consumers.py file

websocket_urlpatterns = [
    re_path(r'ws/stt_pos/$', consumers.STTPOSEndpoint.as_asgi()),
]