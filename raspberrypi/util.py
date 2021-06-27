import queue
from datetime import time


class RGBA:

    def __init__(self, r: int, g: int, b: int, a: int):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class Device:

    def __init__(self, id: str, mac: str, rgba: RGBA, timestamp: float):
        self.id = id
        self.mac = mac
        self.rgba = rgba
        self.time = time

    def __repr__(self) -> str:
        return f"device with mac id {self.id} and mac address {self.mac}, registered at {time.ctime(self.time)}"


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