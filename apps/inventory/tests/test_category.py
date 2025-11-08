from apps.inventory.models import Category, Inventory
from rest_framework import status
from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_category_create(auth_client,urls_cats,):
    response = auth_client.post(urls_cats['category-list'],{'name':'ByCycle'},format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_category_delete(auth_client,urls_cats): 
    response = auth_client.delete(urls_cats['category-detail'])
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_category_delete_with_inventory(auth_client,test_user,urls_cats,category): 
    inventory = Inventory.objects.create(user=test_user,name='Test1',category=category,priority='High',number=3)
    response = auth_client.delete(urls_cats['category-detail'])
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_category_edit(auth_client,urls_cats,category):
    response = auth_client.patch(urls_cats['category-detail'],{'name':'ByCycleEdit'},format='json')
    assert response.status_code == status.HTTP_200_OK

    category.refresh_from_db()
    assert  category.name == 'ByCycleEdit'

@pytest.mark.django_db
def test_category_edit_after_added_inventory(auth_client,test_user,urls_cats,category):
    inventory = Inventory.objects.create(user=test_user,name='Test1',category=category,priority='High',number=3)
    response = auth_client.patch(urls_cats['category-detail'],{'name':'ByCycleEdit'},format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
     
# Unauthenticated user
@pytest.mark.django_db
def test_category_view_annonmous(api_client,urls_cats,category):
    response = api_client.get(urls_cats['category-list'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_category_create_annonmous(api_client,urls_cats,category):
    response = api_client.post(urls_cats['category-list'],{'name':"Test2"},format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_category_edit_annonmous(api_client,urls_cats,category):
    response = api_client.patch(urls_cats['category-detail'],{'name':'ByCycleEdit'},format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_category_delete_anonmous(api_client,urls_cats,category): 
    response = api_client.delete(urls_cats['category-detail'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
