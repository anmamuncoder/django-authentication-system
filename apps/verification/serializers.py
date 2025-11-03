from rest_framework import serializers
from .models import EmailOTP

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
