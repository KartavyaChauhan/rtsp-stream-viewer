# Architecture decisions

Each stream is represented by a Django model and managed by the process-owning `StreamManager`. A POST returns immediately after the process starts; the manager’s daemon monitor independently watches FFmpeg, broadcasts transitions through Channels, and retries unexpected exits with 2, 4, 8, and 16 second backoff. Removing a stream terminates FFmpeg and deletes its HLS directory.

FFmpeg reads RTSP over TCP and produces short H.264 HLS segments. TCP is selected for camera compatibility and loss recovery; `nobuffer`, `low_delay`, a veryfast preset, short segments, and a small playlist balance latency, CPU, and stability. This approach is browser-compatible and avoids attempting impossible direct RTSP playback.

The React application keeps each card independently stateful. hls.js plays the generated playlist; WebSockets update status and dispatch control events. A failed camera cannot block other cards. The UI is responsive, keyboard-focusable, and includes errors, loading states, reconnect, fullscreen, confirmations, and a stream limit message.

For production, use Redis Channels, a strict camera hostname allowlist, authentication/authorization before granting stream access, TLS/WSS, observability, and shared HLS storage or session affinity. This take-home implementation has no authentication because no identity model was supplied; do not expose it publicly without adding one.
