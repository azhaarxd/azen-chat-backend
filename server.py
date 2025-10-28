import os
import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

users = []

@app.route('/')
def index():
    return '''
    <h1>Azen Chat Server Online</h1>
    <p>Socket.IO is running. Connect via Android or website.</p>
    '''

@socketio.on('user connected')
def on_user_connected(data):
    username = data['username']
    if username not in users:
        users.append(username)
    emit('user list', users, broadcast=True)

@socketio.on('chat message')
def on_message(data):
    emit('chat message', data, broadcast=True)

@socketio.on('typing')
def on_typing(data):
    emit('typing', data, broadcast=True, include_self=False)

@socketio.on('disconnect')
def on_disconnect():
    # Optionally remove user from list (by tracking id)
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"=== Starting chat server on http://0.0.0.0:{port} ===")
    socketio.run(app, host="0.0.0.0", port=port)  # DO NOT USE debug=True, threaded, or allow_unsafe_werkzeug
