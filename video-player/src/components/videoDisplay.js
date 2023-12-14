import React, { useState, useEffect } from 'react';
import VideoPlayer from './videoPlayer';
import Video from './video';

const VideoDisplay = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0);

  // Assuming you have the video URL pattern like 'http://127.0.0.1:40000/data/{segmentIndex}'
  const videoUrl = `http://127.0.0.1:40000/data/${currentSegmentIndex}`;

  useEffect(() => {
    // Load the initial segment
    loadSegment(currentSegmentIndex);
  }, [currentSegmentIndex]);

  const loadSegment = async (segmentIndex) => {
    try {
      setLoading(true);
      setError(false);

      // Make a request for the video segment
      const response = await fetch(`http://127.0.0.1:40000/data/${segmentIndex}`);
      console.log(segmentIndex)
      // const data = await response.json();

      // Additional logic to handle the response, update state, etc.

      setLoading(false);
    } catch (error) {
      setError(true);
      setLoading(false);
      console.error('Error loading segment:', error);
    }
  };

  const handleVideoEnd = () => {
    // Increment the segment index when the video ends
    console.log('aaaaa\n\n\n\nend')
    setCurrentSegmentIndex(currentSegmentIndex + 1);
  };

  const renderVideoContent = () => {
    if (loading || error) {
      return <Video />;
    } else {
      return <VideoPlayer videoUrl={videoUrl} onEnd={handleVideoEnd} />;
    }
  };

  return <div>{renderVideoContent()}</div>;
};

export default VideoDisplay;
