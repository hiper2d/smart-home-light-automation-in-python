import json
import threading

from flask import Flask, render_template, request, Response

from raspberrypi.mqtt_client import MqttClient
from raspberrypi.util import MessageAnnouncer

app = Flask(__name__)
mqtt_client = MqttClient()
announcer = MessageAnnouncer()


def format_sse(client_id: str, event=None) -> str:
    msg = {'id': client_id, 'event': event}
    return json.dumps(msg) + '\n\n'


def _on_device_added(device_id: str):
    announcer.announce(format_sse(client_id=device_id))


def _on_device_removed(device_id: str):
    announcer.announce(format_sse(client_id=device_id, event='remove'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('On') == 'ON':
            mqtt_client.send_light_command_to_clients(b'on')
        elif request.form.get('Off') == 'OFF':
            mqtt_client.send_light_command_to_clients(b'off')
        else:
            print('unknown')
    elif request.method == 'GET':
        form = request.form
        return render_template('index.html', form=form, devices=mqtt_client.get_active_client_ids())
    return render_template('index.html')


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield 'data: %s\n\n' % msg
    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    mqtt_client = MqttClient()
    mqtt_client.start()
    mqtt_client.on_device_added = _on_device_added
    mqtt_client.on_device_removed = _on_device_removed
    threading.Thread(target=mqtt_client.clean_dead_devices, daemon=True).start()
    while not mqtt_client.connected:
        pass
    app.run(host='0.0.0.0')