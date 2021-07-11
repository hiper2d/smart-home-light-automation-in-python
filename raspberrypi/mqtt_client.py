import time
from datetime import datetime
from typing import Dict

import paho.mqtt.client as mqtt_client

from util import Device

default_client_id = 'Raspberry Pi Server'
ping_sub = 'home/ping'
host_ip = '192.168.1.36'


class MqttClient:

    def __init__(self, client_id=default_client_id):
        client = mqtt_client.Client(client_id)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        self.client = client
        self.connected = False
        self.devices: Dict[str, Device] = {}
        self.on_device_updated = None
        self.on_device_removed = None

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
            device: Device = Device.string_payload_to_device(message.payload.decode())
            if device.id not in self.devices:
                print(f"Registering new device {device}")
                self.devices[device.id] = device
                if self.on_device_updated:
                    self.on_device_updated(device, 'add')
            else:
                print(f"Updating device: {device}")
                self.devices[device.id].last_updated_at = device.last_updated_at
                if self.devices[device.id].rgb[0] != device.rgb[0] or \
                        self.devices[device.id].rgb[1] != device.rgb[1] or \
                        self.devices[device.id].rgb[2] != device.rgb[2]:
                    self.devices[device.id].rgb = device.rgb
                    if self.on_device_updated:
                        self.on_device_updated(self.devices[device.id])

    def start(self):
        self.client.loop_start()
        self.client.connect(host_ip)

    def send_light_command_to_clients(self, msg: str):
        for device_id, device in self.devices.items():
            device.rgb = msg.split(',')
            self.send_light_command_to_client(device_id, msg)

    def send_light_command_to_client(self, device_id: str, msg: str):
        topic = f"home/{device_id}"
        self.client.publish(topic, msg)
        self.devices[device_id].rgb = msg.split(',')
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def subscribe_to_ping_messages_from_client(self, topic=ping_sub):
        self.client.subscribe(topic)

    def clean_dead_devices(self):
        while True:
            time.sleep(30)
            print(f"Refreshing {len(self.devices.keys())} devices")
            refreshed_devices: Dict[str, Device] = {}
            for device_id, device in self.devices.items():
                print((datetime.now() - device.last_updated_at).seconds)
                if (datetime.now() - device.last_updated_at).seconds > 30:
                    print(f"Device {device_id} is offline")
                    if self.on_device_removed:
                        self.on_device_removed(device)
                else:
                    refreshed_devices[device_id] = device
            self.devices = refreshed_devices


