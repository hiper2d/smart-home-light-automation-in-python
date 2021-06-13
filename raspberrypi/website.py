import threading

from flask import Flask, render_template, request

from raspberrypi.mqtt_client import MqttClient


app = Flask(__name__)


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
        return render_template('index.html', form=form)

    return render_template('index.html')


if __name__ == '__main__':
    mqtt_client = MqttClient()
    mqtt_client.start()
    threading.Thread(target=mqtt_client.clean_dead_devices, daemon=True).start()
    while not mqtt_client.connected:
        pass
    app.run(host='0.0.0.0')