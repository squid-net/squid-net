from flask import Flask, request, make_response, Response
from flask_socketio import SocketIO, emit
import redis
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
redis_pubsub = redis_client.pubsub()
redis_pubsub.subscribe('names')


@app.route('/admin')
def admin():
    return app.send_static_file('admin.html')

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

def event_stream():

    for message in redis_pubsub.listen():
        yield f"data: {message['data']}"

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


if __name__ == "__main__":
    socketio.run(app, host = 'localhost', port = 6969, debug=True)