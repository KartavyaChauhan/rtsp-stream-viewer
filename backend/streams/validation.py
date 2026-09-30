import ipaddress
from urllib.parse import urlparse, urlunparse
from django.conf import settings

class StreamValidationError(ValueError): pass

def validate_rtsp_url(value: str) -> str:
    if not isinstance(value, str) or len(value) > 2048 or any(c in value for c in "\r\n\x00"):
        raise StreamValidationError("Enter a valid RTSP URL.")
    parsed = urlparse(value)
    if parsed.scheme not in {"rtsp", "rtsps"} or not parsed.hostname:
        raise StreamValidationError("URL must use rtsp:// or rtsps:// and include a host.")
    host = parsed.hostname.lower()
    try:
        address = ipaddress.ip_address(host)
        if (address.is_private or address.is_loopback or address.is_link_local) and host not in settings.RTSP_ALLOWED_HOSTS:
            raise StreamValidationError("Private network camera addresses are not allowed by this deployment.")
    except ValueError:
        pass
    if settings.RTSP_ALLOWED_HOSTS and host not in settings.RTSP_ALLOWED_HOSTS:
        raise StreamValidationError("This camera host is not allowed.")
    return value

def sanitize_rtsp_url(value: str) -> str:
    parsed = urlparse(value)
    host = parsed.hostname or "camera"
    port = f":{parsed.port}" if parsed.port else ""
    return urlunparse((parsed.scheme, host + port, parsed.path or "/", "", "", ""))
