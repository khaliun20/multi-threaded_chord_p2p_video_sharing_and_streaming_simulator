import React, { useState, useEffect } from 'react';
import VideoPlayer from './videoPlayer';
import Video from './video'; // Import your Video component

const VideoDisplay = () => {
  const [videoUrls, setVideoUrls] = useState([]);
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchVideoUrls = async () => {
      try {
        const response = await fetch('http://your-api-endpoint/videos'); // Replace with your actual API endpoint
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setVideoUrls(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching video URLs:', error);
        setLoading(false);
        setError(true);
      }
    };
    fetchVideoUrls();
  }, []);

  useEffect(() => {
    if (videoUrls.length > 0) {
      const playNextVideo = () => {
        setCurrentVideoIndex((prevIndex) => (prevIndex + 1) % videoUrls.length);
      };
      const intervalId = setInterval(playNextVideo, 5000); // Play the next video every 5 seconds
      return () => clearInterval(intervalId);
    }
  }, [videoUrls]);

  const renderVideoContent = () => {
    if (loading || error) {
      return <Video />;
    } else if (videoUrls.length > 0) {
      return <VideoPlayer videoUrl={videoUrls[currentVideoIndex]} />;
    } else {
      return <div>No videos available.</div>;
    }
  };

  return <div>{renderVideoContent()}</div>;
};

export default VideoDisplay;
