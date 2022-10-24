from django.urls import re_path

from .consumers import AsyncCryptoConsumer

websocket_urlpatterns = [
    re_path(r'ws/crypto/$', AsyncCryptoConsumer.as_asgi()),
]
