from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Stream
from .services.stream_manager import manager

class StreamConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.stream_id = self.scope["url_route"]["kwargs"]["stream_id"]
        if not await Stream.objects.filter(id=self.stream_id).aexists(): await self.close(code=4404); return
        self.group = f"stream_{self.stream_id}"; await self.channel_layer.group_add(self.group, self.channel_name); await self.accept()
        stream = await Stream.objects.aget(id=self.stream_id); await self.send_json({"type": "stream.status", "status": stream.status, "error_code": stream.error_code, "message": stream.error_message})
    async def disconnect(self, code):
        if hasattr(self, "group"): await self.channel_layer.group_discard(self.group, self.channel_name)
    async def receive_json(self, content):
        action = content.get("action") if isinstance(content, dict) else None
        if action == "pause":
            stream = await Stream.objects.aget(id=self.stream_id); await sync_to_async(manager.set_status)(stream, Stream.Status.PAUSED)
        elif action == "play":
            stream = await Stream.objects.aget(id=self.stream_id); await sync_to_async(manager.set_status)(stream, Stream.Status.LIVE)
        elif action == "reconnect": await sync_to_async(manager.reconnect)(self.stream_id)
        else: await self.send_json({"type": "stream.error", "code": "INVALID_MESSAGE", "message": "Unsupported stream action."})
    async def stream_status(self, event): await self.send_json(event["payload"])
