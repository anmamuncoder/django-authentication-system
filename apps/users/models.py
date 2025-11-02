from django.db import models
from django.contrib.auth.models import User, AbstractUser,AbstractBaseUser
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    is_phone_verify = models.BooleanField(default=False,verbose_name='phone verify')
    is_email_verify = models.BooleanField(default=False,verbose_name='email verify')
    photo = models.ImageField(upload_to='users/',blank=True,null=True)
