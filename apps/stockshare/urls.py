from django.urls import path , include 
from apps.stockshare.views import ShareWithView
from rest_framework.routers import DefaultRouter

router  = DefaultRouter()
router.register('inventory', ShareWithView, basename='share_me')

app_name = 'stockshare'

urlpatterns = (
    [ 
       path('share/', include(router.urls))
    ]   
)

