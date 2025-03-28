from flask_socketio import emit
from app import socketio

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'user': 'Server', 'text': 'Welcome to the chat!'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('send_message')
def handle_send_message(data):
    # Broadcast the incoming message to all connected clients
    socketio.emit('message', data)
