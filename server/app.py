from flask import Flask, request
import redis
import json

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
@app.route('/<name>')
def hello(name):
    ip_address = request.remote_addr
    user_data = {
        'name': name,
        'ip': ip_address
    }
    redis_client.publish('names', json.dumps(user_data))
    return f"Hello {name}!"