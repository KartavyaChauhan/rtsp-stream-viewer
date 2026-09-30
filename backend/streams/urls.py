from django.urls import path
from . import views
urlpatterns = [path("health/", views.health), path("streams/", views.stream_list), path("streams/<uuid:stream_id>/connect/", views.stream_connect), path("streams/<uuid:stream_id>/disconnect/", views.stream_disconnect), path("streams/<uuid:stream_id>/playlist/<str:filename>", views.playlist), path("streams/<uuid:stream_id>/", views.stream_detail)]
