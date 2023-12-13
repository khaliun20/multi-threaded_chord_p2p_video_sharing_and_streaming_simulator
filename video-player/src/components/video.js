import React from 'react';
import Button from 'react-bootstrap/Button';
import './video.css';
import Dropdown from "./dropdown";
import WebSocketComponent from "./websocket";
import { PlayFill } from 'react-bootstrap-icons';
import DataFetcher from "./fetcher";


function Video() {
  return (
    <div className="container my-4">
      <div className="row">
        <div className="col-lg-8 mx-auto">
          <div className="video-mockup" style={{backgroundColor: 'black'}}>
            <div className="video-content" style={{color: 'white'}}>
              <DataFetcher />
            </div>
            <div className="video-controls">
              <Button variant="outline-primary" className="control-item" style={{ backgroundColor: 'transparent', borderColor: 'transparent' }}>
                <PlayFill color="white"/>
              </Button>
            </div>
            <Dropdown />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Video;
