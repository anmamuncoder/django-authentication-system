from django.urls import path,re_path
from apps.stockshare.consumers.share_consumer import ShareConsumer,InventoryConsumer

websocket_urlpatterns = (
    [
        path("ws/stock/share/", ShareConsumer.as_asgi()),
        re_path(r"ws/inventories/(?P<username>[A-Za-z0-9._-]+)/$", InventoryConsumer.as_asgi()),
        
    ]
)
