import React, { useRef, useEffect } from 'react';

const VideoPlayer = ({ videoUrl, onEnd }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    const handleEnded = () => {
      if (onEnd) {
        onEnd();
      }
    };

    const playVideo = async () => {
      try {
        // Attempt to play the video
        await videoRef.current.play();
      } catch (error) {
        // Ignore the play() interruptions
        if (
          error.name === 'NotAllowedError' ||
          error.name === 'AbortError'
        ) {
          console.warn('Play request was interrupted:', error.message);
        } else {
          // Log other errors
          console.error('Error playing video:', error);
        }
      }
    };

    if (videoRef.current) {
      videoRef.current.src = videoUrl;
      videoRef.current.load();

      // Attach the event listener for the video ending
      videoRef.current.addEventListener('ended', handleEnded);

      // Start playing the video automatically
      playVideo();
    }

    // Cleanup: Remove the event listener when the component unmounts
    return () => {
      if (videoRef.current) {
        videoRef.current.removeEventListener('ended', handleEnded);
      }
    };
  }, [videoUrl, onEnd]);

  return (
    <video controls autoPlay ref={videoRef}>
      Your browser does not support the video tag.
    </video>
  );
};

export default VideoPlayer;
