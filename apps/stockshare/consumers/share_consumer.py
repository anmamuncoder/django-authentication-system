import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

class ShareConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Optional: group per user or global
        self.group_name = "stockshare"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
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
