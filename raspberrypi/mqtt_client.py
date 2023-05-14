import time, os
from datetime import datetime
from typing import Dict

import paho.mqtt.client as mqtt_client

from util import Device

mqtt_host = os.getenv('MQTT_HOST', 'localhost')
default_client_id = 'Raspberry Pi Server'
ping_sub = 'home/ping'


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
            remote_device: Device = Device.string_payload_to_device(message.payload.decode())
            if remote_device.id not in self.devices:
                print(f"Registering new device {remote_device}")
                self.devices[remote_device.id] = remote_device
                if self.on_device_updated:
                    self.on_device_updated(remote_device, 'add')
            else:
                local_device = self.devices[remote_device.id]
                local_device.last_updated_at = remote_device.last_updated_at
                print(f"{local_device.on} vs {remote_device.on}")
                if local_device.on != remote_device.on or \
                        local_device.rgba[0] != remote_device.rgba[0] or \
                        local_device.rgba[1] != remote_device.rgba[1] or \
                        local_device.rgba[2] != remote_device.rgba[2]:
                    self.__sync_devices_when_updating(local_device, remote_device)

    def __sync_devices_when_updating(self, local_device: Device, remote_device: Device):
        local_device.on = remote_device.on
        local_device.rgba = remote_device.rgba
        if self.on_device_updated:
            self.on_device_updated(local_device)

    def start(self):
        self.client.loop_start()
        print(mqtt_host)
        self.client.connect(mqtt_host, 1883)

    def send_light_command_to_clients(self, on: bool, rgba_str: str):
        for device_id, device in self.devices.items():
            device.rgba = rgba_str.split(',')
            device.on = on
            self.send_light_command_to_client(device_id, device)

    def send_light_command_to_client(self, device_id: str, device: Device):
        topic = f"home/{device_id}"
        self.devices[device_id].rgba = device.rgba
        self.devices[device_id].on = device.on
        device_json = device.to_json()
        result = self.client.publish(topic, device_json)
        status = result[0]
        if status == 0:
            if self.on_device_updated:
                self.on_device_updated(device, 'update')
            print(f"Send `{device_json}` to topic `{topic}`")
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
                if (datetime.now() - device.last_updated_at).seconds > 30:
                    print(f"Device {device_id} is offline")
                    if self.on_device_removed:
                        self.on_device_removed(device)
                else:
                    refreshed_devices[device_id] = device
            self.devices = refreshed_devices


