import React, { useRef, useEffect } from 'react';

const VideoPlayer = ({ videoUrl }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.src = videoUrl;
    }
  }, [videoUrl]);

  return (
    <video controls ref={videoRef}>
      Your browser does not support the video tag.
    </video>
  );
};

export default VideoPlayer;
