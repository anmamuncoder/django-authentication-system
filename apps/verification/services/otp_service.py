from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta  
from apps.verification.tasks import send_email_task
from apps.verification.models import EmailOTP
import random 

class OTPService:  
    """
    model: Django model to store OTP
    """
    model = EmailOTP # {requrirement field : user, otp}
    template_name = 'otp_email.html'
    otp_expiry_minutes = 10  
    otp_length = 6  

    @classmethod
    def generate_otp(cls):
        return str(random.randint(10**(cls.otp_length-1), 10**cls.otp_length - 1))
    
    @classmethod
    def create_otp(cls,user):
        otp = cls.generate_otp()
        cls.model.objects.create(user=user,otp=otp)
        return True, otp

    @classmethod
    def send_otp(cls,user, celery=False):
        created , otp = cls.create_otp(user)

        # send message with use celery
        if celery:
            send_email_task.delay(user_id=user.id,otp=otp)
            return True

        # send message without use celery
        message = render_to_string(cls.template_name, {"user": user, "otp": otp})
        email = EmailMessage(subject="Your OTP Code",body=message,to=[user.email])
        email.content_subtype = "html"  
        email.send(fail_silently=False)
        return True
    
    @classmethod
    def verify_otp(cls, user, otp):
        try:
            otp_obj = cls.model.objects.filter(user=user,otp=otp,is_verified=False).latest('created_at')
        except cls.model.DoesNotExist:
            return False, "Invalid OTP"

        if timezone.now() > otp_obj.created_at + timedelta(minutes=cls.otp_expiry_minutes):
            return False, "OTP expired"

        otp_obj.is_verified = True
        otp_obj.save()
        
        if hasattr(user, 'is_email_verify'): 
            user.is_email_verify = True
            user.save(update_fields=['is_email_verify'])

        return True, "OTP verified successfully"
    
    @classmethod
    def is_otp_verified(cls, user):
        return cls.model.objects.filter(user= user,is_verified=True).order_by('-created_at').first()
    
    