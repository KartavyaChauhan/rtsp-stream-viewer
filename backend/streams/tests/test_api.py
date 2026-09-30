import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from streams.models import Stream

pytestmark = pytest.mark.django_db

@pytest.fixture
def client(): return APIClient()

@patch("streams.views.manager.start")
def test_create_sanitizes_credentials(start, client):
    response=client.post("/api/streams/", {"url":"rtsp://user:secret@camera.example/live","name":"Gate"}, format="json")
    assert response.status_code == 201
    assert "secret" not in str(response.data)
    assert response.data["safe_url"] == "rtsp://camera.example/live"

def test_rejects_invalid_protocol(client):
    assert client.post("/api/streams/", {"url":"https://example.com"}, format="json").status_code == 400

@patch("streams.views.manager.start")
def test_limit(start, client, settings):
    settings.MAX_ACTIVE_STREAMS = 1
    client.post("/api/streams/", {"url":"rtsp://one.example/live"}, format="json")
    assert client.post("/api/streams/", {"url":"rtsp://two.example/live"}, format="json").status_code == 429

@patch("streams.views.manager.stop")
def test_delete_stops_process(stop, client):
    stream=Stream.objects.create(name="A",stream_url="rtsp://a.example/live",safe_url="rtsp://a.example/live")
    assert client.delete(f"/api/streams/{stream.id}/").status_code == 204
    stop.assert_called_once()
