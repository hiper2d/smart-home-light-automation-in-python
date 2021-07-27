import network
import gc
gc.collect()

ssid = 'Simona2G'
password = '<put you WiFi pass here>'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
