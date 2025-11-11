from django.db import models
from django.contrib.auth.models import User, AbstractUser,BaseUserManager
# Create your models here.
import uuid
 
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=36,unique=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    is_phone_verify = models.BooleanField(default=False,verbose_name='phone verify')
    is_email_verify = models.BooleanField(default=False,verbose_name='email verify')
    photo = models.ImageField(upload_to='users/',blank=True,null=True)
 
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number']  

    objects = UserManager()

    def __str__(self):
        return self.email