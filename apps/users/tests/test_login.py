from rest_framework import status
import pytest

@pytest.mark.django_db
def test_user_login(api_client, test_user, urls):
    login_data = {'username': test_user.username, 'password': 'StrongPass123!'}
    response = api_client.post(urls['login'], login_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_login_invalid_credentials(api_client, test_user, urls):
    login_data = {'username': test_user.username, 'password': 'WrongPass!'}
    response = api_client.post(urls['login'], login_data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
