# API and WebSocket protocol

All REST responses are JSON. Credentials in submitted RTSP URLs are never returned.

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/api/health/` | GET | Server and FFmpeg availability |
| `/api/streams/` | GET | List streams |
| `/api/streams/` | POST | Create and start a stream (`{"url":"rtsp://…","name":"Gate"}`) |
| `/api/streams/{id}/` | GET, DELETE | Inspect or remove and stop a stream |
| `/api/streams/{id}/connect/` | POST | Start a disconnected stream |
| `/api/streams/{id}/disconnect/` | POST | Stop it |
| `/api/streams/{id}/playlist/{file}` | GET | HLS manifest or segment used by the video player |

Creation returns `201` and a stream object containing `id`, `name`, `safe_url`, `status`, reconnect count and `playback_url`. Invalid URLs return `400`; capacity returns `429`; missing streams return `404`.

Connect to `/ws/streams/{id}/`. The server emits `{"type":"stream.status","status":"connecting"}` and later `live`, `reconnecting`, `disconnected`, or `error`. Send one of `{"action":"play"}`, `{"action":"pause"}`, or `{"action":"reconnect"}`. Unsupported JSON results in a `stream.error` event.
