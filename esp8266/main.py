from umqttsimple import MQTTClient
import machine
import time
from machine import Pin

mqtt_server = '192.168.1.36'

client_id = 'Nuffy Module'
topic_sub = b'testTopic'

def sub_cb(topic, msg):
    print(msg)
    led = Pin(2, Pin.OUT)
    led.off()
    time.sleep(0.5)
    led.on()

client = MQTTClient(client_id, mqtt_server)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)

while True:
    client.check_msg()
    time.sleep(1)
