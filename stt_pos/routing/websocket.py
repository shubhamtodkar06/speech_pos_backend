# stt_pos/routing/websocket.py
from django.urls import re_path
from stt_pos import consumers  # Import consumers directly from the app

websocket_urlpatterns = [
    re_path(r'ws/stt_pos/$', consumers.STTPOSEndpoint.as_asgi()),
]