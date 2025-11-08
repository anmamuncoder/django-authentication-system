from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.inventory.models import Category,Inventory
from apps.users.models import User

import pytest
import uuid

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
def urls_cats(category): 
    urls = {
        # Category urls
        'category-list': reverse('inventory:category'),
        'category-detail': reverse('inventory:category-detail', args=[category.id]),   
    }
    return urls

@pytest.fixture
def urls_inve(inventory): 
    urls = { 
        'inventory-list': reverse('inventory:inventory-list'),
        'inventory-detail': reverse('inventory:inventory-detail', args=[inventory.id]),
    }
    return urls

@pytest.fixture
def category(test_user):
    cat = Category.objects.create(user=test_user,name='ByCycle')
    return cat

@pytest.fixture
def inventory(test_user,category):
    inv = Inventory.objects.create(user=test_user,name='Google Pixel',category=category,priority='High',number=2)
    return inv
