import React, { useState, useEffect } from 'react';

const WebSocketComponent = () => {
  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('connecting'); // 'connecting', 'open', 'closed', 'error'

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:40000');

    socket.addEventListener('open', () => {
      setConnectionStatus('open');
    });

    socket.addEventListener('message', (event) => {
      const newMessage = event.data;
      setMessages(prevMessages => [...prevMessages, newMessage]);
    });

    socket.addEventListener('close', () => {
      setConnectionStatus('closed');
    });

    socket.addEventListener('error', () => {
      setConnectionStatus('error');
    });

    return () => {
      // socket.open();
    };
  }, []);

  return (
    <div>
      {connectionStatus === 'connecting' && <div>Waiting on server...</div>}
      {connectionStatus === 'open' && <div>Connected to server.</div>}
      {connectionStatus === 'closed' && <div>Connection closed.</div>}
      {connectionStatus === 'error' && <div>Error connecting to server.</div>}

      {messages.map((message, index) => (
        <div key={index}>{message}</div>
      ))}
    </div>
  );
};

export default WebSocketComponent;
