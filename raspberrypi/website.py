import json
import os.path
import threading
from typing import List, Union, Dict

from flask import Flask, render_template, request, Response, make_response, jsonify
import flask_cors

from mqtt_client import MqttClient
from util import MessageAnnouncer, Device

template_dir = os.path.abspath('static')
app = Flask(__name__, template_folder=template_dir, static_url_path='', static_folder=template_dir)
cors = flask_cors.CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
mqtt_client = MqttClient()
announcer = MessageAnnouncer()


def format_sse(client: Device, event: str = None) -> str:
    device_dict = client.to_dict()
    device_dict['event'] = event
    return json.dumps(device_dict) + '\n\n'


def _on_device_updated(client: Device, event: str = 'update'):
    announcer.announce(format_sse(client=client, event=event))


def _on_device_removed(client: Device):
    announcer.announce(format_sse(client=client, event='remove'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/device', methods=['GET'])
def get_devices():
    devices_as_list: List[Device] = list(mqtt_client.devices.values())
    devices_as_json = list(map(lambda d: d.to_dict(), devices_as_list))
    return make_response(jsonify(devices_as_json), 200)


@app.route('/api/device', methods=['PUT'])
def save_device():
    device: Device = Device.dict_payload_to_device(request.json)
    mqtt_client.send_light_command_to_client(device.id, device)
    response_data = {'message': f'Sent MQTT message to set {device.rgba} color to {device.id}', 'code': 'SUCCESS'}
    return make_response(jsonify(response_data), 200)


@app.route('/api/toggle', methods=['GET'])
def toggle_all():
    rgba = request.args.get('rgba')
    on = True if request.args.get('on') == 'true' else False
    mqtt_client.send_light_command_to_clients(on, rgba)
    data = {'message': f'Sent MQTT message to set {rgba} color to all devices', 'code': 'SUCCESS'}
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
    app.run(host='0.0.0.0', port=5002)