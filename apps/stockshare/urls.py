from django.urls import path , include
from apps.stockshare.views import ShareWithView

urlpatterns = (
    [
        path('api/share/',ShareWithView.as_view(),name='share_me'),
        
    ] 
)

