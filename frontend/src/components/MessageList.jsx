import React from 'react';

const MessageList = ({ messages }) => {
  return (
    <ul className="message-list">
      {messages.map((msg, index) => (
        <li key={index}>
          <strong>{msg.user}: </strong>{msg.text}
        </li>
      ))}
    </ul>
  );
};

export default MessageList;
