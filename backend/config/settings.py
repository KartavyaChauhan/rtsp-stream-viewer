import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-development-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [v.strip() for v in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if v.strip()]
INSTALLED_APPS = ["daphne", "django.contrib.contenttypes", "django.contrib.auth", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "corsheaders", "rest_framework", "channels", "streams"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS = [v.strip() for v in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",") if v.strip()]
CORS_ALLOW_CREDENTIALS = False
MAX_ACTIVE_STREAMS = int(os.getenv("MAX_ACTIVE_STREAMS", "4"))
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
RTSP_ALLOWED_HOSTS = {v.strip().lower() for v in os.getenv("RTSP_ALLOWED_HOSTS", "").split(",") if v.strip()}
REDIS_URL = os.getenv("REDIS_URL", "")
CHANNEL_LAYERS = {"default": {"BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": {"hosts": [REDIS_URL]}}} if REDIS_URL else {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
