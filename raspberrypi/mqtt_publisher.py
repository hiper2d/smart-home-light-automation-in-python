import paho.mqtt.client as mqtt_client
import json

default_client_id = 'Alex Mac'
light_pub = 'home/light'
register_sub = 'home/register'
host_ip = '192.168.1.36'


class MqttClient:
    def __init__(self, client_id=default_client_id):
        client = mqtt_client.Client(client_id)
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        self.client = client
        self.connected = False
        self.devices = []

    def __on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected to MQTT Broker")
            self.subscribe()
        else:
            print("Failed to connect, return code %d\n", rc)

    def __on_message(self, client, userdata, message: mqtt_client.MQTTMessage):
        print(f"Received `{message.payload}` from `{message.topic}`")
        if message.topic == register_sub:
            self.devices.append(message.payload.decode())
            print(self.devices)

    def start(self):
        self.client.loop_start()
        self.client.connect(host_ip)

    def publish(self, msg, topic=light_pub):
        for device in self.devices:
            result = self.client.publish("home/" + device, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

    def subscribe(self, topic=register_sub):
        self.client.subscribe(topic)


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
        mqtt_client.publish(inp)

