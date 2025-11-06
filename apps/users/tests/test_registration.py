from rest_framework import status
from apps.users.models import User
import pytest

@pytest.mark.django_db
def test_user_registration(api_client, user_data, urls):
    response = api_client.post(urls['register'], user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data

@pytest.mark.django_db
def test_duplicate_email_registration(api_client, user_data, urls):
    User.objects.create_user(username='duplicate', email=user_data['email'], password='StrongPass123!')
    response = api_client.post(urls['register'], user_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data
