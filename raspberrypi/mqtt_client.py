import time
from typing import Dict

import paho.mqtt.client as mqtt_client

default_client_id = 'Raspberry Pi Server'
ping_sub = 'home/ping'
host_ip = '192.168.1.36'


class Device:
    def __init__(self, mac: str, time: float):
        self.mac = mac
        self.time = time

    def __repr__(self) -> str:
        return f"device with mac address: {self.mac}, registered at {time.ctime(self.time)}"


class MqttClient:
    def __init__(self, client_id=default_client_id):
        client = mqtt_client.Client(client_id)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        self.client = client
        self.connected = False
        self.devices: Dict[str, Device] = {}

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected to MQTT Broker\n")
            self.subscribe_to_ping_messages_from_client()
        else:
            print("Failed to connect, return code %d\n", rc)

    def _on_message(self, client, userdata, message: mqtt_client.MQTTMessage):
        print(f"Received `{message.payload}` from `{message.topic}`")
        if message.topic == ping_sub:
            payload = message.payload.decode()
            [client_id, mac] = payload.split("|")
            if client_id not in self.devices:
                print(f"Registering new device {client_id}")
            self.devices[client_id] = Device(mac, time.time())

    def start(self):
        self.client.loop_start()
        self.client.connect(host_ip)

    def send_light_command_to_clients(self, msg: bytes):
        for device in self.devices.keys():
            topic = f"home/{device}"
            result = self.client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg.decode()}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

    def subscribe_to_ping_messages_from_client(self, topic=ping_sub):
        self.client.subscribe(topic)

    def clean_dead_devices(self):
        while True:
            time.sleep(30)
            print(f"Refreshing {len(self.devices.keys())} devices")
            refreshed_devices: Dict[str, Device] = {}
            for key, value in self.devices.items():
                if time.time() - value.time > 30:
                    print(f"Device {key} is offline")
                else:
                    refreshed_devices[key] = value
            self.devices = refreshed_devices


