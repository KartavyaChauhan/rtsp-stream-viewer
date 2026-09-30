import logging
import shutil
import subprocess
import threading
import time
from pathlib import Path
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from ..models import Stream
from .ffmpeg import command

logger = logging.getLogger(__name__)

class StreamManager:
    """Owns FFmpeg processes; no HTTP request waits for a camera process."""
    def __init__(self): self.processes = {}; self.lock = threading.RLock()
    def output_dir(self, stream_id): return Path(settings.MEDIA_ROOT) / "hls" / str(stream_id)
    def notify(self, stream: Stream):
        async_to_sync(get_channel_layer().group_send)(f"stream_{stream.id}", {"type": "stream.status", "payload": {"type": "stream.status", "status": stream.status, "error_code": stream.error_code, "message": stream.error_message, "reconnects": stream.reconnects}})
    def set_status(self, stream, status, code="", message=""):
        stream.status, stream.error_code, stream.error_message = status, code, message
        stream.save(update_fields=["status", "error_code", "error_message", "updated_at"])
        self.notify(stream)
    def start(self, stream_id, retry=False):
        key = str(stream_id)
        with self.lock:
            if key in self.processes: return
            stream = Stream.objects.get(id=stream_id)
            folder = self.output_dir(stream_id)
            shutil.rmtree(folder, ignore_errors=True)
            folder.mkdir(parents=True, exist_ok=True)
            self.set_status(stream, Stream.Status.RECONNECTING if retry else Stream.Status.CONNECTING)
            try: process = subprocess.Popen(command(stream.stream_url, folder), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            except FileNotFoundError: self.set_status(stream, Stream.Status.ERROR, "FFMPEG_NOT_FOUND", "FFmpeg is not installed on the server."); return
            except OSError: self.set_status(stream, Stream.Status.ERROR, "PROCESS_START_FAILED", "Unable to start the stream process."); return
            self.processes[key] = process
            threading.Thread(target=self.monitor, args=(stream_id, process), daemon=True).start()
    def monitor(self, stream_id, process):
        key = str(stream_id)
        playlist = self.output_dir(stream_id) / "index.m3u8"
        deadline = time.monotonic() + 12
        while process.poll() is None and not playlist.exists() and time.monotonic() < deadline:
            time.sleep(0.25)
        if playlist.exists() and process.poll() is None:
            stream = Stream.objects.filter(id=stream_id).first()
            if stream: self.set_status(stream, Stream.Status.LIVE)
        elif process.poll() is None:
            process.terminate()
        process.wait()
        stderr = process.stderr.read().decode("utf-8", errors="replace")[-2000:] if process.stderr else ""
        stream = Stream.objects.filter(id=stream_id).first()
        if stream and stderr:
            # Keep credentials server-side even in diagnostic logs.
            logger.warning("ffmpeg_exited stream=%s code=%s stderr=%s", stream.id, process.returncode, stderr.replace(stream.stream_url, stream.safe_url))
        with self.lock:
            if self.processes.get(key) is not process: return
            self.processes.pop(key, None)
        if not stream or stream.status == Stream.Status.DISCONNECTED: return
        if stream.reconnects < 4:
            stream.reconnects += 1; stream.save(update_fields=["reconnects", "updated_at"])
            self.set_status(stream, Stream.Status.RECONNECTING, "FFMPEG_EXITED", "Connection lost; retrying.")
            time.sleep(min(2 ** stream.reconnects, 16)); self.start(stream_id, True)
        else: self.set_status(stream, Stream.Status.ERROR, "FFMPEG_EXITED", "The camera connection ended after several retries.")
    def stop(self, stream_id):
        with self.lock: process = self.processes.pop(str(stream_id), None)
        if process and process.poll() is None:
            process.terminate()
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired: process.kill(); process.wait()
        stream = Stream.objects.filter(id=stream_id).first()
        if stream: self.set_status(stream, Stream.Status.DISCONNECTED)
        shutil.rmtree(self.output_dir(stream_id), ignore_errors=True)
    def reconnect(self, stream_id): self.stop(stream_id); self.start(stream_id, True)

manager = StreamManager()
