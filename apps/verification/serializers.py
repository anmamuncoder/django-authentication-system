from rest_framework import serializers
from .models import EmailOTP
from apps.users.models import User 

class EmailOTPCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        request = self.context['request']
        user = request.user
         
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
 
        if attrs['email'] != user.email:
            raise serializers.ValidationError("Email does not match the authenticated user.")

        return attrs

class EmailOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


# ------------------------------------------------
# Forget Password for Anonimous User
# ------------------------------------------------

# Request for OTP 
class ForgotPasswordOTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email): 
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("No account found with this email.")
        return email

# Verify OPT
class ForgotPasswordOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

 