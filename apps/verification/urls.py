from django.urls import path , include
from .views import SendOTPView,VerifyOTPView ,ForgotPasswordSendOTPView, ForgotPasswordVerifyOTPView,ResetPasswordView

app_name = 'verification' 

urlpatterns = (
    [
        path('email/verify/request/',SendOTPView.as_view(),name='request-verify'),
        path('email/verify/conform/',VerifyOTPView.as_view(),name='conform-verify'),

        path("password/forgot/otp/request/", ForgotPasswordSendOTPView.as_view(),name='forgot-password-send-otp'),
        path("password/forgot/otp/conform/", ForgotPasswordVerifyOTPView.as_view(),name='forgot-password-verify-otp'),
        path("password/forgot/reset/", ResetPasswordView.as_view(),name='forgot-password-reset'),
    ]  
)