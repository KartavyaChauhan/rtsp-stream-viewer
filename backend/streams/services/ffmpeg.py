from pathlib import Path
from django.conf import settings

def command(stream_url: str, output_dir: Path) -> list[str]:
    # `-timeout` is supported by the RTSP demuxer shipped in the Docker image.
    # `-rw_timeout` is not accepted by recent Debian FFmpeg builds.
    return [settings.FFMPEG_PATH, "-nostdin", "-hide_banner", "-loglevel", "warning", "-rtsp_transport", "tcp", "-timeout", "10000000", "-fflags", "nobuffer", "-flags", "low_delay", "-i", stream_url, "-an", "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency", "-g", "48", "-f", "hls", "-hls_time", "2", "-hls_list_size", "5", "-hls_flags", "delete_segments+append_list+independent_segments", "-hls_segment_filename", str(output_dir / "segment_%05d.ts"), str(output_dir / "index.m3u8")]
