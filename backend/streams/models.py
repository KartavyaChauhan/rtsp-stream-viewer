import uuid
from django.db import models

class Stream(models.Model):
    class Status(models.TextChoices):
        IDLE = "idle"; CONNECTING = "connecting"; LIVE = "live"; PAUSED = "paused"; RECONNECTING = "reconnecting"; DISCONNECTED = "disconnected"; ERROR = "error"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    stream_url = models.URLField(max_length=2048)
    safe_url = models.CharField(max_length=2048)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.IDLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reconnects = models.PositiveIntegerField(default=0)
    error_code = models.CharField(max_length=40, blank=True)
    error_message = models.CharField(max_length=255, blank=True)
