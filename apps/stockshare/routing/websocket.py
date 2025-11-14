from django.urls import path
from apps.stockshare.consumers.share_consumer import ShareConsumer

websocket_urlpatterns = (
    [
        path("ws/stock/share/", ShareConsumer.as_asgi()),
        
    ]
)
