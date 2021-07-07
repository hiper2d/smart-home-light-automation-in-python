from __future__ import annotations

import datetime
import json
import queue
from typing import Dict, Union, List


class Device:

    @staticmethod
    def string_payload_to_device(payload: str) -> Device:
        device_dict = json.loads(payload)
        return Device(**device_dict)

    def __init__(self, id: str, mac: str, rgb: [int], timestamp: datetime = datetime.datetime.now()):
        self.id = id
        self.mac = mac
        self.rgb = rgb
        self.created_at = timestamp

    def to_dict(self) -> Dict['str', Union[str, List[int]]]:
        return {'id': self.id, 'rgb': self.rgb, 'on': True}

    def __repr__(self) -> str:
        return f"device with mac id {self.id} and mac address {self.mac}, " \
               f"registered at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


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
