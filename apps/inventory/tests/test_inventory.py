from apps.inventory.models import Category,Inventory
from rest_framework import status
import pytest

@pytest.mark.django_db
def test_inventory_create(auth_client,test_user,urls_inve,category):
    response = auth_client.post(urls_inve['inventory-list'],{"user":test_user.id,"name":"TestInventory","category":category.id,"priority":"Low","number":3},format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_inventory_update(auth_client,test_user,urls_inve,category):
    new_category = Category.objects.create(user=test_user,name='TestInventoryUpdate')
    response = auth_client.patch(urls_inve['inventory-detail'],{"name":"TestInventoryPatch","category":new_category.id,"priority":"High","number":4},format='json')
 
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "TestInventoryPatch"
    assert response.data['priority'] == "High"
    assert str(response.data['category']) == str(new_category.id)

@pytest.mark.django_db
def test_inventory_delete(auth_client,test_user,urls_inve):
    response = auth_client.delete(urls_inve['inventory-detail'])
    assert response.status_code == status.HTTP_204_NO_CONTENT

# Test for Anonmous
@pytest.mark.django_db
def test_inventory_create_annonmous(api_client,test_user,urls_inve,category):
    response = api_client.post(urls_inve['inventory-list'],{"user":test_user.id,"name":"TestInventory","category":category.id,"priority":"Low","number":3},format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_inventory_update_annonmous(api_client,test_user,urls_inve,category):
    new_category = Category.objects.create(user=test_user,name='TestInventoryUpdate')
    response = api_client.patch(urls_inve['inventory-detail'],{"name":"TestInventoryPatch","category":new_category.id,"priority":"High","number":4},format='json')
 
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

