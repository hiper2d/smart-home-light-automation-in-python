import paho.mqtt.client as mqtt_client


default_client_id = 'Alex Mac'
test_topic = 'testTopic'
host_ip = '192.168.1.36'


class MqttClient():
    def __init__(self, client_id=default_client_id):
        client = mqtt_client.Client(client_id)
        client.on_connect = self.__on_connect
        self.client = client
        self.connected = False

    def __on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def start(self):
        self.client.loop_start()
        self.client.connect(host_ip)

    def publish_to_topic(self, msg, topic=test_topic):
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


if __name__ == "__main__":
    mqtt_client = MqttClient()
    mqtt_client.start()
    while not mqtt_client.connected:
        pass
    inp: str = ''
    while inp != 'exit':
        inp = input("Print a message to send: ")
        if inp == 'exit':
            pass
        mqtt_client.publish_to_topic(inp)

