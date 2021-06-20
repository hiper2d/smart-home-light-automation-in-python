import json
import threading
import os.path

from flask import Flask, render_template, request, Response, send_from_directory, make_response, jsonify
from flask_cors import CORS

from raspberrypi.mqtt_client import MqttClient
from raspberrypi.util import MessageAnnouncer

template_dir = os.path.abspath('public')
app = Flask(__name__, template_folder=template_dir, static_url_path='/', static_folder=template_dir)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
mqtt_client = MqttClient()
announcer = MessageAnnouncer()


def format_sse(client_id: str, event=None) -> str:
    msg = {'id': client_id, 'event': event}
    return json.dumps(msg) + '\n\n'


def _on_device_added(device_id: str):
    announcer.announce(format_sse(client_id=device_id))


def _on_device_removed(device_id: str):
    announcer.announce(format_sse(client_id=device_id, event='remove'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/device', methods=['GET'])
def device():
    return make_response(jsonify(mqtt_client.get_active_client_ids()), 200)


@app.route('/toggle', methods=['GET'])
def toggle_all():
    operation = request.args.get('operation')
    if operation == 'on':
        mqtt_client.send_light_command_to_clients(b'on')
    elif operation == 'off':
        mqtt_client.send_light_command_to_clients(b'off')
    else:
        print('Unknown operation ' + operation)
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield 'data: %s\n\n' % msg
    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    # try:
    #     mqtt_client = MqttClient()
    #     mqtt_client.start()
    #     mqtt_client.on_device_added = _on_device_added
    #     mqtt_client.on_device_removed = _on_device_removed
    #     threading.Thread(target=mqtt_client.clean_dead_devices, daemon=True).start()
    #     while not mqtt_client.connected:
    #         pass
    # except:
    #     print('Cannot connect to MQTT broker')
    app.run(host='0.0.0.0')