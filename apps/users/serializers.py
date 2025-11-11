from rest_framework import serializers
from .models import User
from django.contrib.auth import password_validation
from apps.verification.services.otp_service import OTPService

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','phone_number','photo')
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value
    
    def update(self, instance, validated_data):
        old_email = instance.email
        user = super().update(instance, validated_data)
        OTPService.send_otp(user, celery=False)
        new_email = validated_data.get('email')
        if new_email and new_email != old_email:  # After change email is_email_verify will false
            user.is_email_verify = False
            user.save(update_fields=['is_email_verify'])
        
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate_new_password(self, value):
        # Django password validators
        password_validation.validate_password(value)
        return value
