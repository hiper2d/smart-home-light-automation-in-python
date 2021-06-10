from umqttsimple import MQTTClient
import machine
import time
import ubinascii
from machine import Pin

mqtt_server = '192.168.1.36'

client_id = ubinascii.hexlify(machine.unique_id())
light_sub = b'home/light'
register_pub = b'home/register'
led = Pin(2, Pin.OUT)


def sub_cb(topic, msg):
    print(msg)
    if msg == b'on':
        led.off()
    else:
        led.on()


client = MQTTClient(client_id, mqtt_server)
client.set_callback(sub_cb)
client.connect()
client.publish(register_pub, client_id)
client.subscribe(b"home/" + client_id)

while True:
    client.check_msg()
    time.sleep(1)