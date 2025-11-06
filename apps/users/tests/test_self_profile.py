import pytest
from rest_framework import status
from apps.users.models import User

@pytest.mark.django_db
def test_get_self_profile(auth_client, test_user, urls):
    response = auth_client.get(urls['self_me'])
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == test_user.username

@pytest.mark.django_db
def test_update_self_profile_put(auth_client, test_user, urls):
    update_data = {'username':'username','first_name': 'Updated', 'last_name': 'User', 'email': 'newemail@example.com'}
    response = auth_client.put(urls['self_me'], update_data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not User.objects.get(id=test_user.id).is_email_verify

@pytest.mark.django_db
def test_update_self_profile_patch(auth_client, test_user, urls):
    response = auth_client.patch(urls['self_me'], {'first_name': 'Patched'}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert User.objects.get(id=test_user.id).first_name == 'Patched'

@pytest.mark.django_db
def test_delete_self_profile(auth_client, test_user, urls):
    response = auth_client.delete(urls['self_me'])
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=test_user.id).exists()

@pytest.mark.django_db
def test_post_self_profile_not_allowed(auth_client, urls):
    response = auth_client.post(urls['self_me'], {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
