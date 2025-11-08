from django.urls import path , include
from .views import CategoryView,InventoryView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('inventory',InventoryView)

app_name = 'inventory' 
urlpatterns = (
    [ 
        path('category/',CategoryView.as_view(),name='category'),
        path('category/<uuid:id>/',CategoryView.as_view(),name='category-detail'),

    ]   + router.urls
)