from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from langchain_openai import ChatOpenAI

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Removed the unsupported 'use_responses_api' parameter.
llm = ChatOpenAI(model="gpt-4o-mini")

def transform_message(raw_message):
    if 'user' in raw_message and 'text' in raw_message:
        # Convert the 'user' key to the 'role' key, and 'text' to 'content'
        return {"role": raw_message['user'].lower(), "content": raw_message['text']}
    return raw_message

# Helper function to process a user message via LangChain.
def process_message(message):
    # Append the new user message (already transformed) to the conversation history.
    MESSAGES.append(message)
    
    # Ensure all messages in conversation_context have the required keys.
    conversation_context = []
    for msg in MESSAGES:
        if 'role' not in msg or 'content' not in msg:
            msg = transform_message(msg)
        conversation_context.append(msg)
    
    try:
        response = llm.invoke(conversation_context)
        assistant_message = response.text()
        MESSAGES.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    except Exception as e:
        print("Error processing message:", e)
        return "Error processing message."

# Existing REST endpoints
MESSAGES = []

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(MESSAGES), 200

@app.route('/api/messages', methods=['POST'])
def post_message():
    message = request.get_json()
    # Transform the message to have 'role' and 'content' keys.
    transformed_message = transform_message(message)
    MESSAGES.append(transformed_message)
    return jsonify(transformed_message), 201

@app.route('/api/ai', methods=['POST'])
def process_ai_message():
    data = request.get_json()
    raw_message = data.get('message')
    if not raw_message:
        return jsonify({"error": "No message provided"}), 400

    # Transform the raw message to the expected format.
    message = transform_message(raw_message)

    ai_response = process_message(message)
    return jsonify({"response": ai_response}), 200

# SocketIO event handlers for real-time chat
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    try:
        emit('message', {'user': 'Server', 'text': 'Welcome to the chat!'})
    except ConnectionResetError as e:
        print("ConnectionResetError on connect:", e)

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('send_message')
def handle_send_message(data):
    try:
        print("Received message:", data)
        MESSAGES.append(data)
        # Exclude the sender from the broadcast
        socketio.emit('message', data, include_self=False)
    except ConnectionResetError as e:
        print("ConnectionResetError in send_message:", e)

@socketio.on_error_default
def default_error_handler(e):
    print("SocketIO error:", e)

if __name__ == '__main__':
    socketio.run(app, debug=True)
