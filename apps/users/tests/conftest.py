from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from apps.users.models import User
import pytest

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username='existinguser',
        email='existing@example.com',
        password='StrongPass123!'
    )
    user.is_email_verify = True
    user.save()
    return user

@pytest.fixture
def unverify_user(db):
    user = User.objects.create_user(
        username='unverifyuser',
        email='unverify@example.com',
        password='StrongPass123!'
    )
    return user

@pytest.fixture
def access_token(test_user):
    refresh = RefreshToken.for_user(test_user)
    return str(refresh.access_token)

@pytest.fixture
def auth_client(api_client, access_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client
    
@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'phone_number': '1234567890',
        'password': 'StrongPass123!'
    }

@pytest.fixture
def urls():
    return {
        'register': reverse('users:register'),
        'login': reverse('users:login'),
        'login_refresh': reverse('users:login-refresh'),
        'self_me': reverse('users:self-me'),
        'change_password': reverse('users:change-password')
    }
