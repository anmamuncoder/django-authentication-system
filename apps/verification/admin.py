from django.contrib import admin
from .models import EmailOTP
# Register your models here.

@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['id','user_email','otp','created_at','is_verified','is_expired']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User Email"
