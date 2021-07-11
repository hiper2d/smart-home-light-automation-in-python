import json
import os.path
import threading
from typing import List, Union, Dict

from flask import Flask, render_template, request, Response, make_response, jsonify
from flask_cors import CORS

from mqtt_client import MqttClient
from util import MessageAnnouncer, Device

template_dir = os.path.abspath('public')
app = Flask(__name__, template_folder=template_dir, static_url_path='', static_folder=template_dir)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
mqtt_client = MqttClient()
announcer = MessageAnnouncer()


def format_sse(client: Device, event: str = None) -> str:
    msg = {'id': client.id, 'rgb': client.rgb, 'event': event}
    return json.dumps(msg) + '\n\n'


def _on_device_updated(client: Device, event: str = 'update'):
    announcer.announce(format_sse(client=client, event=event))


def _on_device_removed(client: Device):
    announcer.announce(format_sse(client=client, event='remove'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/device', methods=['GET'])
def device():
    devices_as_list: List[Device] = list(mqtt_client.devices.values())
    devices_as_json = list(map(lambda d: d.to_dict(), devices_as_list))
    print(devices_as_json)
    return make_response(jsonify(devices_as_json), 200)


@app.route('/api/toggle/<client_id>', methods=['GET'])
def toggle_one (client_id: str):
    rgb = request.args.get('rgb')
    mqtt_client.send_light_command_to_client(client_id, rgb)
    data = {'message': f'Sent MQTT message to set {rgb} color to {client_id}', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)


@app.route('/api/toggle', methods=['GET'])
def toggle_all():
    rgb = request.args.get('rgb')
    mqtt_client.send_light_command_to_clients(rgb)
    data = {'message': f'Sent MQTT message to set {rgb} color to all devices', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)


@app.route('/api/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield 'data: %s\n\n' % msg
    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    try:
        mqtt_client = MqttClient()
        mqtt_client.start()
        mqtt_client.on_device_updated = _on_device_updated
        mqtt_client.on_device_removed = _on_device_removed
        threading.Thread(target=mqtt_client.clean_dead_devices, daemon=True).start()
        while not mqtt_client.connected:
            pass
    except:
        print('Cannot connect to MQTT broker')
    app.run(host='0.0.0.0')