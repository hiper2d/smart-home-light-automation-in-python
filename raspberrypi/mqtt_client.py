import json
import time
from collections import namedtuple
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Dict, List

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
        self.on_device_added = None
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
            if self.on_device_added:
                self.on_device_added(device)

    def start(self):
        self.client.loop_start()
        self.client.connect(host_ip)

    def send_light_command_to_clients(self, msg: str):
        for device in self.devices.keys():
            self.send_light_command_to_client(device, msg)

    def send_light_command_to_client(self, device_id: str, msg: str):
        topic = f"home/{device_id}"
        self.client.publish(topic, msg)
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
                if (datetime.now() - device.created_at).seconds > 30:
                    print(f"Device {device_id} is offline")
                    if self.on_device_removed:
                        self.on_device_removed(device)
                else:
                    refreshed_devices[device_id] = device
            self.devices = refreshed_devices


