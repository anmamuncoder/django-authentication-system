from django.urls import path , include
from .views import SendOTPView,VerifyOTPView
urlpatterns = (
    [
        path('me/email/request-verify/',SendOTPView.as_view(),name='request-verify'),
        path('me/email/conform-verify/',VerifyOTPView.as_view(),name='conform-verify'),
    ]  
)