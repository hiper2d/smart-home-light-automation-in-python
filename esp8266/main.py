from umqttsimple import MQTTClient
from machine import Pin
import machine
import ujson
import ubinascii
import uasyncio as asyncio
import functions


def scale(num: int) -> int:
    return int(num * scale_coefficient * brightness) + 1


def upscale(num: int) -> int:
    return int((num - 1) / scale_coefficient / brightness)


mqtt_server = '192.168.4.49'

client_id = ubinascii.hexlify(machine.unique_id())
mac = ubinascii.hexlify(network.WLAN().config('mac'),':')
print("Started device with client id " + client_id.decode() + " and mac: " + mac.decode())
register_pub = "home/ping"
scale_coefficient: float = 1023 / 255
led = Pin(2, Pin.OUT)
brightness: float = 1.0
rgb = functions.get_colors()
on = False if rgb == [0, 0, 0] else True
r = upscale(rgb[0])
g = upscale(rgb[1])
b = upscale(rgb[2])


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
    if (r == 0 and g == 0 and b == 0) or on is False:
        functions.all_off()
        led.on()
    else:
        functions.choose_color(scale(r), scale(g), scale(b))
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
