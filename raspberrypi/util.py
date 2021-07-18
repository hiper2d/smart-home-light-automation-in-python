from __future__ import annotations

from datetime import datetime
import json
import queue
from typing import Dict, Union, List


class Device:

    @staticmethod
    def string_payload_to_device(payload: str) -> Device:
        device_dict = json.loads(payload)
        new_device = Device(**device_dict)
        new_device.last_updated_at = datetime.now()
        return new_device

    @staticmethod
    def dict_payload_to_device(payload_dict: Dict) -> Device:
        print(payload_dict)
        new_device = Device(**payload_dict)
        new_device.last_updated_at = datetime.now()
        return new_device

    def __init__(self, id: str, rgba: [int], mac: str = '', event: str = None, on: bool = True, timestamp: datetime = datetime.now()):
        self.id = id
        self.mac = mac
        self.rgba = rgba
        self.on = on
        self.event = event
        self.last_updated_at = timestamp

    def to_dict(self) -> Dict['str', Union[str, List[int]]]:
        return {'id': self.id, 'rgba': self.rgba, 'on': self.on}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def rgba_str(self):
        [r, g, b, a] = self.rgba
        return f"{r},{g},{b}.{a}"

    def __repr__(self) -> str:
        return f"device with mac id {self.id}, on status {self.on}, rgba {self.rgba} " \
               f"last updated at {self.last_updated_at.strftime('%Y-%m-%d %H:%M:%S')}"


class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]
