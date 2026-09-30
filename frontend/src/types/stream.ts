export type StreamStatus = 'idle'|'connecting'|'live'|'paused'|'reconnecting'|'disconnected'|'error';
export interface Stream { id:string; name:string; safe_url:string; status:StreamStatus; created_at:string; reconnects:number; error_code:string; error_message:string; playback_url:string; }
