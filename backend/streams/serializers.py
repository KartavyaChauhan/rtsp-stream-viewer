from rest_framework import serializers
from .models import Stream
from .validation import StreamValidationError, sanitize_rtsp_url, validate_rtsp_url

class StreamSerializer(serializers.ModelSerializer):
    playback_url = serializers.SerializerMethodField()
    class Meta:
        model = Stream
        fields = ["id", "name", "safe_url", "status", "created_at", "updated_at", "reconnects", "error_code", "error_message", "playback_url"]
        read_only_fields = fields
    def get_playback_url(self, obj): return f"/api/streams/{obj.id}/playlist/index.m3u8"

class StreamCreateSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=2048, write_only=True)
    name = serializers.CharField(max_length=80, required=False, allow_blank=True)
    def validate_url(self, value):
        try: return validate_rtsp_url(value)
        except StreamValidationError as error: raise serializers.ValidationError(str(error))
    def create(self, data):
        url = data["url"]
        name = data.get("name", "").strip() or f"Camera {Stream.objects.count() + 1}"
        return Stream.objects.create(name=name, stream_url=url, safe_url=sanitize_rtsp_url(url))
