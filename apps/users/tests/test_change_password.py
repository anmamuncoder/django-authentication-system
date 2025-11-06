import pytest
from rest_framework import status

@pytest.mark.django_db
def test_change_password_success(auth_client, test_user, urls):
    data = {'old_password': 'StrongPass123!', 'new_password': 'NewStrongPass123!'}
    response = auth_client.post(urls['change_password'], data, format='json')
    assert response.status_code == status.HTTP_200_OK
    test_user.refresh_from_db()
    assert test_user.check_password('NewStrongPass123!')

@pytest.mark.django_db
def test_change_password_wrong_old_password(auth_client, test_user, urls):
    data = {'old_password': 'WrongOldPass', 'new_password': 'NewStrongPass123!'}
    response = auth_client.post(urls['change_password'], data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'old_password' in response.data
    
# ------------------------------
# Email un-verify user
# ------------------------------
@pytest.mark.django_db
def test_unverify_user_change_password(api_client,unverify_user,urls):
    data = {'old_password': 'StrongPass123!', 'new_password': 'NewStrongPass123!'}
    response = api_client.post(urls['change_password'], data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED