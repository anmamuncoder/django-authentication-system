from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Inventory
from apps.stockshare.serializers import InventorySerializerUUIDtoSTRING
from apps.users.models import User
from django.db import models
from datetime import datetime

def get_user_inventories(user):
    qs = Inventory.objects.filter(models.Q(user=user) | models.Q(user__shared_connections__shared_user=user)).distinct()
    serializers = InventorySerializerUUIDtoSTRING(qs, many=True)
    return serializers.data

def broadcast_inventory_update(instance, event_type):
    channel_layer = get_channel_layer()
    # Owners
    owners = {instance.user}

    # Shared users
    shared_users = instance.user.shared_connections.all().values_list("shared_user", flat=True)
    shared_users_qs = User.objects.filter(id__in=shared_users)
    receivers = owners.union(set(shared_users_qs))

    for user in receivers: 
        async_to_sync(channel_layer.group_send)(f"user_{user.username}",
            {
                "type": "inventory_event",
                "event": event_type,
                "data": get_user_inventories(user),
                "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

@receiver(post_save, sender=Inventory)
def inventory_saved(sender, instance, created, **kwargs):
    event_type = "created" if created else "updated"
    broadcast_inventory_update(instance, event_type)

@receiver(post_delete, sender=Inventory)
def inventory_deleted(sender, instance, **kwargs):
    broadcast_inventory_update(instance, "deleted")
