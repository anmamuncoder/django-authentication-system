from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from .serializers import ( EmailOTPCreateSerializer, EmailOTPVerifySerializer, 
                          ForgotPasswordOTPRequestSerializer,ForgotPasswordOTPVerifySerializer,ResetPasswordSerializer )
from .models import EmailOTP
from apps.verification.services.otp_service import OTPService
from apps.users.models import User 
from .throttles import RequstVerifyThrottle
# Create your views here.
  

class SendOTPView(APIView):
    serializer_class = EmailOTPCreateSerializer 
    throttle_classes = [RequstVerifyThrottle]
    throttle_scope = 'request_verify'
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        OTPService.send_otp(user=user,celery=False)
      
        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    serializer_class = EmailOTPVerifySerializer 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        success, message = OTPService.verify_otp(user, otp)
        if not success:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh = str(refresh)

        return Response({"access": access, "refresh": refresh}, status=status.HTTP_200_OK)



# ------------------------------------------------
# Forget Password For Anonimous User
# ------------------------------------------------

# Request for OTP : 
class ForgotPasswordSendOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordOTPRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        OTPService.send_otp(user) 

        return Response({"detail": "OTP sent to email"}, status=200)
    
# Verify OPT
class ForgotPasswordVerifyOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordOTPVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        user = User.objects.get(email=email)

        success, message = OTPService.verify_otp(user, otp)
        if not success:
            return Response({"detail": message}, status=400)

        return Response({"detail": message}, status=200)
 
# Reset Change Passwort
class ResetPasswordView(APIView):
    permission_classes = []
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        user = User.objects.get(email=email)

        success, message = OTPService.verify_otp(user, otp)
        otp_obj = OTPService.is_otp_verified(user)
        if not otp_obj or otp_obj.otp != otp:
            return Response({"detail": "OTP not verified or expired"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password reset successful"}, status=200)
