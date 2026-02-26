from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws://localhost:8000/ws/jogo/
    re_path(r'ws/jogo/$', consumers.JogoConsumer.as_asgi()),
]