from django.db import models  
import uuid
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
# Create your models here.

class EmailOTP(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_otps')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)  # valid for 10 min

    def __str__(self):
        return f"{self.user.email} - {self.otp}"
