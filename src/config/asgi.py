import os

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application

from polygon import routing as polygon_routing
from polygon import consumers as polygon_consumers


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(
        polygon_routing.websocket_urlpatterns
    ),
    "channel": ChannelNameRouter({
        "polygon": polygon_consumers.AsyncPolygonConsumer.as_asgi()
    })
})
