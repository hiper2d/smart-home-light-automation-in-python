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


def light_message_callback(topic: str, msg: bytes):
    print("Received message from server: " + msg.decode())
    [r, g, b] = msg.decode().split(',')
    if r == '0' and g == '0' and b == '0':
        functions.all_off()
        led.on()
    else:
        functions.choose_color(int(r), int(g), int(b))
        led.off()


async def main_loop():
    while True:
        client.check_msg()
        await asyncio.sleep(1)


async def ping_loop():
    while True:
        rgb = functions.get_colors()
        device = {'id': client_id, 'mac': mac, 'rgb': rgb}
        device_json = ujson.dumps(device)
        client.publish(register_pub, device_json)
        print("Sending ping massage to server " + device_json)
        await asyncio.sleep(15)


client = MQTTClient(client_id, mqtt_server)
client.set_callback(light_message_callback)
client.connect()
client.subscribe(b'home/' + client_id)

asyncio.create_task(main_loop())
asyncio.create_task(ping_loop())
loop = asyncio.get_event_loop()
loop.run_forever()

led.off()
