import React from 'react';
import Button from 'react-bootstrap/Button';
import './video.css';

function Video() {
  return (
    <div className="container my-4">
      <div className="row">
        <div className="col-lg-8 mx-auto">
          <div className="video-mockup">
            <div className="video-content">
              <p>Your text goes here. It can be anything you want to display.</p>
            </div>
            <div className="video-controls">
              <Button variant="primary" className="control-item">Play</Button>
              <Button variant="secondary" className="control-item">Pause</Button>
              <Button variant="info" className="control-item">Volume</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Video;
