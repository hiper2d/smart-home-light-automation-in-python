from umqttsimple import MQTTClient
from machine import Pin
import machine
import ujson
import ubinascii
import uasyncio as asyncio
import functions

mqtt_server = '192.168.1.36'

client_id = ubinascii.hexlify(machine.unique_id())
mac = ubinascii.hexlify(network.WLAN().config('mac'),':')
print("Started device with client id " + client_id.decode() + " and mac: " + mac.decode())
register_pub = "home/ping"
led = Pin(2, Pin.OUT)
brightness: float = 1.0
on = True
[r,g,b] = functions.get_colors()


def light_message_callback(topic: str, msg: bytes):
    global r, g, b, brightness, on
    json = msg.decode()
    print("Received message from server: " + json)
    dict_from_json = ujson.loads(json)
    on = dict_from_json['on']
    [r_str, g_str, b_str, a_str] = dict_from_json['rgba']
    r = int(r_str)
    g = int(g_str)
    b = int(b_str)
    brightness = float(a_str)
    if r == 0 and g == 0 and b == 0:
        functions.all_off()
        led.on()
    else:
        functions.choose_color(r, g, b)
        led.off()
    publish()


async def main_loop():
    while True:
        client.check_msg()
        await asyncio.sleep(0.2)


async def ping_loop():
    while True:
        publish()
        await asyncio.sleep(15)

def publish():
    device = {'id': client_id, 'on': on, 'mac': mac, 'rgba': [r,g,b,brightness]}
    device_json = ujson.dumps(device)
    client.publish(register_pub, device_json)
    print("Sending ping massage to server " + device_json)


client = MQTTClient(client_id, mqtt_server)
client.set_callback(light_message_callback)
client.connect()
client.subscribe(b'home/' + client_id)

asyncio.create_task(main_loop())
asyncio.create_task(ping_loop())
loop = asyncio.get_event_loop()
loop.run_forever()

led.off()
