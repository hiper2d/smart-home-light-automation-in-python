from flask import Flask, render_template, request

from raspberrypi.mqtt_publisher import MqttClient

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('On') == 'ON':
            print('on')
            mqtt_client.publish_to_topic('on')
        elif  request.form.get('Off') == 'OFF':
            print('off')
            mqtt_client.publish_to_topic('off')
        else:
            print('unknown')
    elif request.method == 'GET':
        form = request.form
        return render_template('index.html', form=form)

    return render_template('index.html')


if __name__ == '__main__':
    mqtt_client = MqttClient()
    mqtt_client.start()
    while not mqtt_client.connected:
        pass
    app.run(debug=True, host='0.0.0.0')