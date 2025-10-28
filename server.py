from flask import Flask, render_template
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
    users.append(username)
    emit('user list', users, broadcast=True)

@socketio.on('chat message')
def on_message(data):
    emit('chat message', data, broadcast=True)

@socketio.on('typing')
def on_typing(data):
    emit('typing', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    print("=== Starting chat server on http://0.0.0.0:5000 ===")
    socketio.run(app, host='0.0.0.0', port=5000)
