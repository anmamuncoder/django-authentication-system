import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
# Models
from apps.stockshare.models import ShareWith
# Fixture
from apps.users.tests.factories import UserFactory
from apps.stockshare.tests.factories import ShareWithFactory
# Create your tests here.

# ------------------------------
# Test Fixture
# ------------------------------

pytestmark = pytest.mark.django_db

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def auth_client(client,user):
    user.is_email_verify = True
    user.save()
    client.force_authenticate(user=user)
    return client
  
@pytest.fixture
def url():
    return reverse("stockshare:share_me-list")


# ------------------------
# Test View
# ------------------------
def test_sharewith_user_connection_list(auth_client,url,user):
    """
    Test that for view list of connection
    Return HTTP 200 OK
    """
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    
def test_sharewith_user_connection_crate_vice_versa(auth_client,url,user):
    """
    Test that for connection create successfully!
    Return HTTP 201 CREATED
    """
    user2 = UserFactory()    
    response = auth_client.post(url,{"shared_user":user2.username},format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Ensure vice-versa connections are created 
    has_user1 = ShareWith.objects.filter(owner=user,shared_user=user2).exists()
    has_user2 = ShareWith.objects.filter(owner=user2,shared_user=user).exists()
    assert has_user1 is True
    assert has_user2 is True

def test_sharewith_cannot_create_duplicate_connection(auth_client,url,user):
    """
    Test for duplicate conneciton controll
    If already same youser connected so will not again connet the same user
    Return HTTP 403 FORBIDDEN 
    """
    user2 = UserFactory()

    # First connections
    response = auth_client.post(url,{"shared_user":user2.username},format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Second Connections will block
    response = auth_client.post(url,{"shared_user":user2.username},format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_sharewith_delete_connection_by_non_owner_returns_404(auth_client,url,user):
    """
    Test that a user cannot delete a ShareWith connection they do not own.
    Expect a 404 Not Found response, since the object is not in the requesting user's queryset.
    """
    user2 = UserFactory()
    user3 = UserFactory()

    # By Authenticated - created connection 
    data = ShareWith.objects.create(owner=user2,shared_user=user3)

    # By UnAuthenticated - Delete connection
    delete_url = reverse("stockshare:share_me-detail", args=[data.id])
    response = auth_client.delete(delete_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_sharewith_user_connection_delete(auth_client,url,user):
    """
    Test for Ensure vice-versa connections are deleted.
    Return HTTP 204 NO CONTENT
    """
    user2 = UserFactory()

    # POST, user conneciting 
    response = auth_client.post(url,{"shared_user":user2.username},format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Delete using detail URL
    share_id = ShareWith.objects.get(owner=user,shared_user=user2).id
    delete_url = reverse("stockshare:share_me-detail", args=[share_id])
    response = auth_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    has_user1 = ShareWith.objects.filter(owner=user,shared_user=user2).exists()
    has_user2 = ShareWith.objects.filter(owner=user2,shared_user=user).exists()
    assert has_user1 is False
    assert has_user2 is False

def test_sharewith_limited_user_connections(auth_client,url,user):
    """
    Test that for unpaid user can connected limited connection
    Only can will connect within user.connection
    """
    limit = user.connections
    for _ in range(limit):
        demo_user = UserFactory()
        response = auth_client.post(url,{"shared_user":demo_user.username})
        assert response.status_code == status.HTTP_201_CREATED
    
    user2 = UserFactory()
    response = auth_client.post(url,{"shared_user":user2.username})
    assert response.status_code == status.HTTP_403_FORBIDDEN    
 
# ------------------------------
# Test For Unauthenticated User
# ------------------------------

def test_sharewith_unauth_connection_list_block(client,url,user):
    """
    Test for UnAuthenticated user cant view data
    Return HTTP 401 UNAUTHORIZED
    """    
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_sharewith_unauth_connection_create_block(client,url,user):
    """
    Test that for UnAuthenticated user cant create any data
    Return HTTP 401 UNAUTHORIZED
    """
    user2 = UserFactory()

    response = client.post(url,{"shared_user":user2.username})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_sharewith_unauth_connection_delete_block(client,url,user):
    """
    Test that for UnAuthenticated user cant delete any data
    Return HTTP 401 UNAUTHORIZED
    """
    user2 = UserFactory()
    user3 = UserFactory()

    # By Authenticated - created connection 
    data = ShareWith.objects.create(owner=user2,shared_user=user3)

    # By UnAuthenticated - Delete connection
    delete_url = reverse("stockshare:share_me-detail", args=[data.id])
    response = client.delete(delete_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_sharewith_unauth_connection_update_block(client,url,user):
    """
    Test that for UnAuthenticated user cant update put/patch
    Return HTTP 401 UNAUTHORIZED
    """
    user2 = UserFactory()
    user3 = UserFactory()

    # By Authenticated - created connection 
    data = ShareWith.objects.create(owner=user2,shared_user=user3)
    # By UnAuthenticated - Pactch connection
    update_url = reverse("stockshare:share_me-detail", args=[data.id])

    response_patch = client.patch(update_url,{"shared_user":user.username})
    response_put = client.put(update_url,{"shared_user":user.username})

    assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_put.status_code == status.HTTP_401_UNAUTHORIZED
