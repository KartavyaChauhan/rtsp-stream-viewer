import { useEffect, useRef } from 'react';
import Hls from 'hls.js';

type VideoPlayerProps = Readonly<{ src: string; playing: boolean }>;

export function VideoPlayer({ src, playing }: VideoPlayerProps) {
	const ref = useRef<HTMLVideoElement>(null);

	useEffect(() => {
		const video = ref.current;
		if (!video || !playing) {
			return;
		}

		let hls: Hls | undefined;
		if (Hls.isSupported()) {
			hls = new Hls({
				liveSyncDurationCount: 3,
				manifestLoadingMaxRetry: 20,
				manifestLoadingRetryDelay: 1000,
				manifestLoadingMaxRetryTimeout: 4000,
			});
			hls.loadSource(src);
			hls.attachMedia(video);
		} else {
			video.src = src;
		}

		return () => {
			hls?.destroy();
			video.pause();
			video.removeAttribute('src');
			video.load();
		};
	}, [src, playing]);

	useEffect(() => {
		const video = ref.current;
		if (!video) {
			return;
		}

		if (playing) {
			void video.play().catch(() => {});
		} else {
			video.pause();
		}
	}, [playing]);

	return <video ref={ref} muted playsInline aria-label="Live camera video" />;
}
