from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, UserView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)

app_name = 'users'  

router = DefaultRouter() 

urlpatterns =  (
    [
        path('profile/',UserView.as_view(),name='self-me'),
        path("password/change/", ChangePasswordView.as_view(), name="change-password"),
        path('register/',UserRegisterView.as_view(),name='register'),
        path('login/',TokenObtainPairView.as_view(),name="login"),
        path('login/refresh/',TokenRefreshView.as_view(),name="login-refresh"),
         
    ]  + router.urls
)
# path('users/<str:username>/',UserView.as_view(),name='self-me'),
