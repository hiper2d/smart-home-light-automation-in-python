import network
import gc
gc.collect()

ssid = 'SakoWiFi'
password = 'greenpeer742'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
