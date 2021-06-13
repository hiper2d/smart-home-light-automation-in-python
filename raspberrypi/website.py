import threading
from typing import List

from flask import Flask, render_template, request, Response

from raspberrypi.mqtt_client import MqttClient
from raspberrypi.util import MessageAnnouncer

app = Flask(__name__)
mqtt_client = MqttClient()
announcer = MessageAnnouncer()


def _on_message_announce(items: List[str]):
    announcer.announce("ABC")
    print(items)


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
        return render_template('index.html', form=form, devices=mqtt_client.get_devices_as_list())
    return render_template('index.html')


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg
    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    mqtt_client = MqttClient()
    mqtt_client.start()
    mqtt_client.on_message_finalize = _on_message_announce
    threading.Thread(target=mqtt_client.clean_dead_devices, daemon=True).start()
    while not mqtt_client.connected:
        pass
    app.run(host='0.0.0.0')