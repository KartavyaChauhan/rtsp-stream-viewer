import uuid
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="Stream", fields=[
        ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
        ("name", models.CharField(max_length=80)),
        ("stream_url", models.URLField(max_length=2048)),
        ("safe_url", models.CharField(max_length=2048)),
        ("status", models.CharField(max_length=16, choices=[("idle","Idle"),("connecting","Connecting"),("live","Live"),("paused","Paused"),("reconnecting","Reconnecting"),("disconnected","Disconnected"),("error","Error")], default="idle")),
        ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
        ("reconnects", models.PositiveIntegerField(default=0)), ("error_code", models.CharField(max_length=40, blank=True)), ("error_message", models.CharField(max_length=255, blank=True)),
    ])]
