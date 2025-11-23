import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.verification.models import EmailOTP
from apps.users.tests.factories import UserFactory, EmailOTPFactory
from apps.verification.services.otp_service import OTPService

pytestmark = pytest.mark.django_db

# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def auth_client(api_client, user):
    user.is_email_verify = True
    user.save()
    
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def otp_obj(user):
    OTPService.send_otp(user, celery=False)
    return EmailOTP.objects.filter(user=user).last()

# ----------------------------
# Authenticated User OTP
# ---------------------------- 
def test_send_otp(auth_client, user):
    """
    Test that otp request is working properly, properlty generating otp 
    """
    url = reverse('verification:request-verify')
    response = auth_client.post(url, data={'email': user.email})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "OTP sent successfully"
    assert EmailOTP.objects.filter(user=user).exists()
 
def test_verify_otp(auth_client, otp_obj):
    """
    """
    url = reverse('verification:conform-verify')
    response = auth_client.post(url, data={'email': otp_obj.user.email, 'otp': otp_obj.otp})
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data and 'refresh' in response.data


# ----------------------------
# Forgot Password OTP (Anonymous)
# ---------------------------- 
def test_forgot_password_send_otp(api_client, user):
    """
    Test that if user forget his password, then reqeust a otp send his mail address
    """
    url = reverse('verification:forgot-password-send-otp')
    response = api_client.post(url, data={'email': user.email})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "OTP sent to email"
    assert EmailOTP.objects.filter(user=user).exists()

 
def test_forgot_password_verify_otp(api_client, user, otp_obj):
    """
    Test that if user forget his password, and otp verify of this mail
    """
    url = reverse('verification:forgot-password-verify-otp')
    response = api_client.post(url, data={'email': user.email, 'otp': otp_obj.otp})
    assert response.status_code == status.HTTP_200_OK
    assert "OTP verified" in response.data['detail']
 
def test_reset_password(api_client, user, otp_obj):
    """
    Test that after verify top reset his password
    """
    url = reverse('verification:forgot-password-reset')
    data = {
        'email': user.email,
        'otp': otp_obj.otp,
        'new_password': 'NewStrongPass123'
    }
    otp_obj.is_verified = True
    otp_obj.save()
    
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "Password reset successful"

    user.refresh_from_db()
    
    assert user.check_password('NewStrongPass123')
