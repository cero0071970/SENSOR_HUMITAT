"""
# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
#import gc
#gc.collect()


ssid = 'wlanosc'
password = 'Oscar1970'
mqtt_server = 'mqtt.flespi.io'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

print ("connecting")
station.active(True)
print(station.scan())
station.connect(ssid, password)

while station.isconnected() == False:
  print ("connecting")
  #pass

print('Connection successful')
print(station.ifconfig())
"""