import pytest
from django.db import IntegrityError
from django.test import TestCase
# Data Model
from apps.stockshare.models import ShareWith
# Factory Model
from apps.users.tests.factories import UserFactory 
from apps.stockshare.tests.factories import ShareWithFactory

# Create your tests here.

pytestmark = pytest.mark.django_db
 
def test_sharewith_creation():
    """
    Test creating a ShareWith instance with valid owner and shared_user.
    """
    user1 = UserFactory()
    user2 = UserFactory()

    share = ShareWith.objects.create(owner=user1, shared_user=user2)

    assert share.id is not None
    assert share.owner == user1
    assert share.shared_user == user2
    assert str(share) == f"{user1.username} - {user2.username}"

def test_sharewith_unique_constraint():
    """
    Test that creating a duplicate 
    ShareWith instance with the same owner/shared_user raises IntegrityError.
    """
    user1 = UserFactory()
    user2 = UserFactory()

    ShareWith.objects.create(owner=user1, shared_user=user2)

    with pytest.raises(IntegrityError):
        ShareWith.objects.create(owner=user1, shared_user=user2)

def test_sharewith_update_shared_user():
    """
    Test updating the shared_user field of an existing ShareWith instance.
    """
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    share = ShareWith.objects.create(owner=user1, shared_user=user2)

    share.shared_user = user3
    share.save()

    updated = ShareWith.objects.get(id=share.id)
    assert updated.shared_user == user3
    assert updated.owner == user1

def test_sharewith_update_owner():
    """
    Test updating the owner field of an existing ShareWith instance.
    """
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    share = ShareWith.objects.create(owner=user1, shared_user=user2)

    share.owner = user3
    share.save()

    updated = ShareWith.objects.get(id=share.id)
    assert updated.owner == user3
    assert updated.shared_user == user2

def test_sharewith_delete():
    """
    Test deleting a ShareWith instance.
    """
    user1 = UserFactory()
    user2 = UserFactory()

    share = ShareWith.objects.create(owner=user1, shared_user=user2)
    share_id = share.id

    share.delete()

    with pytest.raises(ShareWith.DoesNotExist):
        ShareWith.objects.get(id=share_id)