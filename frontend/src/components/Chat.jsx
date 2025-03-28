import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { v4 as uuidv4 } from 'uuid';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

// Connect to the Socket.IO server
const socket = io('http://localhost:5000');

const Chat = () => {
  const [messages, setMessages] = useState([]);

  // Fetch initial messages from the REST API on component mount
  useEffect(() => {
    fetch('http://localhost:5000/api/messages')
      .then((res) => res.json())
      .then((data) => {
        setMessages(data);
      })
      .catch((err) => console.error('Error fetching messages:', err));
  }, []);

  // Listen for incoming messages from the server via Socket.IO
  useEffect(() => {
    socket.on('message', (message) => {
      // Avoid adding duplicate messages (check by id)
      setMessages((prevMessages) => {
        if (prevMessages.find((msg) => msg.id === message.id)) {
          return prevMessages;
        }
        return [...prevMessages, message];
      });
    });

    // Cleanup listener on unmount
    return () => {
      socket.off('message');
    };
  }, []);

  const handleSend = async (newMessage) => {
    // Assign a unique id to the message
    const messageWithId = { ...newMessage, id: uuidv4() };

    // Immediately update local state so the user sees their message
    setMessages((prevMessages) => [...prevMessages, messageWithId]);
    
    // Emit the message to the server (server broadcasts to other clients)
    socket.emit('send_message', messageWithId);

    // Post the message to the REST endpoint for persistence (optional)
    try {
      await fetch('http://localhost:5000/api/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(messageWithId)
      });
    } catch (error) {
      console.error('Error posting message:', error);
    }

    // Call the AI processing endpoint to get a response
    try {
      const response = await fetch('http://localhost:5000/api/ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: newMessage.text })
      });
      const data = await response.json();
      
      if (data.response) {
        const aiMessage = { user: 'AI', text: data.response, id: uuidv4() };
        // Immediately update local state for the AI response
        setMessages((prevMessages) => [...prevMessages, aiMessage]);
        // Emit the AI message to other clients
        socket.emit('send_message', aiMessage);
      }
    } catch (error) {
      console.error('Error fetching AI response:', error);
    }
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <MessageInput onSend={handleSend} />
    </div>
  );
};

export default Chat;
