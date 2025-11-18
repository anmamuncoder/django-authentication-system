from django.urls import path , include
from apps.stockshare.views import ShareWithView
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register('api/share',ShareWithView,basename='share_me')

urlpatterns = (
    [
        
    ]   + routers.urls
)