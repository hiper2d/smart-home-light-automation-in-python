from umqttsimple import MQTTClient
from machine import Pin
import machine
import time
import ubinascii
import uasyncio as asyncio
import functions

mqtt_server = '192.168.1.36'

client_id = ubinascii.hexlify(machine.unique_id())
mac = ubinascii.hexlify(network.WLAN().config('mac'),':')
print("Started device with client id " + client_id.decode() + " and mac: " + mac.decode())
register_pub = "home/ping"
led = Pin(2, Pin.OUT)


def light_message_callback(topic, msg):
    print("Received message from server: " + msg.decode())
    [r,g,b,a] = msg.decode().split(',')
    if a == '0':
        functions.all_off()
    else:
        functions.choose_color(r, g, b)


async def main_loop():
    while True:
        client.check_msg()
        await asyncio.sleep(1)


async def ping_loop():
    while True:
        msg = client_id + b'|' + mac
        client.publish(register_pub, msg)
        print("Sending ping massage to server " + msg.decode())
        await asyncio.sleep(15)


client = MQTTClient(client_id, mqtt_server)
client.set_callback(light_message_callback)
client.connect()
client.subscribe(b'home/' + client_id)

asyncio.create_task(main_loop())
asyncio.create_task(ping_loop())
loop = asyncio.get_event_loop()
loop.run_forever()


