from django.urls import path, include  
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
) 
urlpatterns =  (
    [
        path('users/login/',TokenObtainPairView.as_view(),name="login"),
        path('users/login/refresh/',TokenRefreshView.as_view(),name="login-refresh"), 
    ]  
)
