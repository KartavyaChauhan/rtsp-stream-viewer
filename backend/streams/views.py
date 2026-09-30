from pathlib import Path
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stream
from .serializers import StreamCreateSerializer, StreamSerializer
from .services.stream_manager import manager

@api_view(["GET", "POST"])
def stream_list(request):
    if request.method == "GET": return Response(StreamSerializer(Stream.objects.all().order_by("-created_at"), many=True).data)
    if Stream.objects.exclude(status=Stream.Status.DISCONNECTED).count() >= settings.MAX_ACTIVE_STREAMS: return Response({"detail": f"Maximum of {settings.MAX_ACTIVE_STREAMS} active streams reached."}, status=429)
    serializer = StreamCreateSerializer(data=request.data); serializer.is_valid(raise_exception=True)
    stream = serializer.save(); manager.start(stream.id)
    return Response(StreamSerializer(stream).data, status=status.HTTP_201_CREATED)

@api_view(["GET", "DELETE"])
def stream_detail(request, stream_id):
    try: stream = Stream.objects.get(id=stream_id)
    except Stream.DoesNotExist: return Response({"detail": "Stream not found."}, status=404)
    if request.method == "DELETE": manager.stop(stream.id); stream.delete(); return Response(status=204)
    return Response(StreamSerializer(stream).data)

@api_view(["POST"])
def stream_connect(request, stream_id):
    stream = Stream.objects.filter(id=stream_id).first()
    if not stream: return Response({"detail": "Stream not found."}, status=404)
    manager.start(stream.id); return Response(StreamSerializer(Stream.objects.get(id=stream.id)).data)

@api_view(["POST"])
def stream_disconnect(request, stream_id):
    stream = Stream.objects.filter(id=stream_id).first()
    if not stream: return Response({"detail": "Stream not found."}, status=404)
    manager.stop(stream.id); return Response(StreamSerializer(Stream.objects.get(id=stream.id)).data)

@api_view(["GET"])
def playlist(request, stream_id, filename):
    if filename != Path(filename).name or not filename.endswith((".m3u8", ".ts")):
        raise Http404("Media not found.")
    path = manager.output_dir(stream_id) / filename
    if not path.exists(): raise Http404("Playback is not ready.")
    content_type = "application/vnd.apple.mpegurl" if filename.endswith(".m3u8") else "video/mp2t"
    return FileResponse(path.open("rb"), content_type=content_type)

@api_view(["GET"])
def health(request):
    import shutil as shell
    return Response({"status": "ok", "ffmpeg": bool(shell.which(settings.FFMPEG_PATH)), "active_streams": Stream.objects.exclude(status=Stream.Status.DISCONNECTED).count()})
