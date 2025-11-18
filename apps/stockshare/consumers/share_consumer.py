import json
from django.core.serializers.json import DjangoJSONEncoder 
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from asgiref.sync import sync_to_async
from django.db import models

class ShareConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Optional: group per user or global
        self.group_name = "stockshare"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # sync_to_async(self.channel_layer.group_add)(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "share_message",
                "data": data,
            }
        )
        
    async def share_message(self, event):
        msg = event["data"] 
        msg["server_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        await self.send(text_data=json.dumps(msg))

    # async def share_message(self, event):
        # await self.send(text_data=json.dumps(event["data"]))
   

class InventoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group  = f"user_{self.username}"  # match signals group

        # Join the users group
        await self.channel_layer.group_add(self.room_group ,self.channel_name)
        await self.accept()

        # Send initial data
        inventories = await self.get_user_inventories(self.username)
        await self.send(json.dumps({
            "type": "initial_data",
            "inventories": inventories
        }, cls=DjangoJSONEncoder))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group ,self.channel_name)

    # Called when signals send 'inventory_event'
    async def inventory_event(self, event):

        await self.send(text_data=json.dumps(
            {
            "type": "inventory_event",
            "event": event["event"],
            "inventories": event["data"]
            }, 
            cls=DjangoJSONEncoder)
        )

    @sync_to_async
    def get_user_inventories(self, username):
        from apps.inventory.models import Inventory
        from apps.users.models import User
        from apps.stockshare.serializers import InventorySerializerUUIDtoSTRING

        user = User.objects.get(username=username)
        qs = Inventory.objects.filter(models.Q(user=user) |models.Q(user__shared_connections__shared_user=user)).distinct()

        serializers = InventorySerializerUUIDtoSTRING(qs,many=True)
        return serializers.data
