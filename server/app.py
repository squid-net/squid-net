from flask import Flask, request
from flask_socketio import SocketIO, emit
import redis
import json

app = Flask(__name__)
socketio = SocketIO(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
@app.route('/<name>')
def index(name):
    ip_address = request.remote_addr
    user_data = {
        'name': name,
        'ip': ip_address
    }
    redis_client.publish('names', json.dumps(user_data))
    return f"Hello {name}!"

if __name__ == "__main__":

    socketio.run(app, host = 'localhost', port = 6969)