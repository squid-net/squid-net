from flask import Flask, request, make_response
from flask_socketio import SocketIO, emit
import redis
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

@app.route('/admin')
def admin():
    return app.send_static_file('admin.html')

@app.route('/')
@app.route('/<name>')
def index(name='anonymous'):
    ip_address = request.remote_addr
    user_data = {
        'name': name,
        'ip': ip_address
    }
    redis_client.publish('names', json.dumps(user_data))

    response = make_response(f"Hello {name}!")

    return response

@socketio.on('connect', namespace='/admin')
def admin_connect():
    print('Client connected to /admin namespace')

@socketio.on('disconnect', namespace='/admin')
def admin_disconnect():
    print('Client disconnected from /admin namespace')

def redis_listener():
    print("Redis listener started")
    pubsub = redis_client.pubsub()
    pubsub.subscribe('names')
    for message in pubsub.listen():
        if message['type'] == 'message':
            name = json.loads(message['data'])['name']
            socketio.emit('new_name', name, namespace='/admin', broadcast=True)

if __name__ == "__main__":
    socketio.start_background_task(redis_listener)
    socketio.run(app, host = 'localhost', port = 6969)