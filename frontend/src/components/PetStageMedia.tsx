import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Box } from '@mui/material';

interface PetStageMediaProps {
  petTemplateId: number;
  stageIndex: number;
  alt: string;
}

export function PetStageMedia({ petTemplateId, stageIndex, alt }: PetStageMediaProps) {
  const imageSrc = `/pets/${petTemplateId}/stage${stageIndex}.png`;
  const videoCandidates = useMemo(
    () => [`/pets/${petTemplateId}/stage${stageIndex}.mp4`, `/pets/${petTemplateId}/stage${stageIndex},mp4`],
    [petTemplateId, stageIndex]
  );

  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageFailed, setImageFailed] = useState(false);
  const [videoReady, setVideoReady] = useState(false);
  const [videoEnabled, setVideoEnabled] = useState(true);
  const [videoIndex, setVideoIndex] = useState(0);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    setImageLoaded(false);
    setImageFailed(false);
    setVideoReady(false);
    setVideoEnabled(true);
    setVideoIndex(0);
  }, [imageSrc, videoCandidates]);

  const currentVideoSrc = videoCandidates[videoIndex];
  const shouldTryVideo = videoEnabled && (imageLoaded || imageFailed);

  const tryPlayVideo = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;
    const playPromise = video.play();
    if (playPromise && typeof playPromise.catch === 'function') {
      playPromise.catch(() => {});
    }
  }, []);

  useEffect(() => {
    if (!shouldTryVideo) return;

    const onBridgeReady = () => {
      tryPlayVideo();
    };

    document.addEventListener('WeixinJSBridgeReady', onBridgeReady as EventListener);
    return () => {
      document.removeEventListener('WeixinJSBridgeReady', onBridgeReady as EventListener);
    };
  }, [shouldTryVideo, currentVideoSrc, tryPlayVideo]);

  const wechatInlineAttrs = useMemo(
    () =>
      ({
        'webkit-playsinline': 'true',
        'x5-playsinline': 'true',
        'x5-video-player-type': 'h5-page',
        'x5-video-player-fullscreen': 'false',
        'x-webkit-airplay': 'allow',
      }) as Record<string, string>,
    []
  );

  return (
    <Box sx={{ position: 'relative', width: '100%', height: '100%' }}>
      {!imageFailed && (
        <Box
          component='img'
          src={imageSrc}
          alt={alt}
          loading='lazy'
          onLoad={() => setImageLoaded(true)}
          onError={() => setImageFailed(true)}
          sx={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            objectPosition: 'center',
            opacity: videoReady ? 0 : 1,
            transition: 'opacity 240ms ease',
          }}
        />
      )}

      {shouldTryVideo && (
        <video
          {...wechatInlineAttrs}
          ref={videoRef}
          key={currentVideoSrc}
          src={currentVideoSrc}
          poster={imageSrc}
          autoPlay
          loop
          muted
          playsInline
          controls={false}
          disablePictureInPicture
          disableRemotePlayback
          controlsList='nodownload nofullscreen noremoteplayback noplaybackrate'
          preload='metadata'
          onLoadedData={() => {
            setVideoReady(true);
            tryPlayVideo();
          }}
          onCanPlay={tryPlayVideo}
          onError={() => {
            if (videoIndex < videoCandidates.length - 1) {
              setVideoIndex((prev) => prev + 1);
              return;
            }
            setVideoEnabled(false);
          }}
          onContextMenu={(e) => e.preventDefault()}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            objectPosition: 'center',
            opacity: videoReady ? 1 : 0,
            transition: 'opacity 240ms ease',
            pointerEvents: 'none',
            userSelect: 'none',
          }}
        />
      )}
    </Box>
  );
}
