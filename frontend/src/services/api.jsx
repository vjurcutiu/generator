// This file abstracts API calls to the Flask backend
const API_URL = 'http://localhost:5000/api';

export const fetchMessages = async () => {
  try {
    const response = await fetch(`${API_URL}/messages`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching messages:', error);
    return [];
  }
};

export const sendMessage = async (message) => {
  try {
    const response = await fetch(`${API_URL}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message)
    });
    return await response.json();
  } catch (error) {
    console.error('Error sending message:', error);
    return message;
  }
};
