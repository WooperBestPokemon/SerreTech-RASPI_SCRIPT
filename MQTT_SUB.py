import paho.mqtt.client as paho #import the client1
from datetime import datetime
import requests
import sys
import time
import json
import LOG
import ALARM

url = 'http://localhost:8000/api/data'

red_light = 17
green_light = 18
blue_light = 27

ALARM.set_light(green_light,red_light)

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

def onMessage(client, userdata, msg):
    
    j = msg.payload.decode()
    p = Payload(j)

    temperature = {'type' : 'Temperature', 'value' : p.temperature}
    humair = {'type' : 'Air Humidity', 'value' : p.humair}
    humsol = {'type' : 'Ground Humidity', 'value' : p.humsol}
    light = {'type' : 'Luminosity', 'value' : p.light}
    
    try:
        w = requests.post(url, data = temperature)
        x = requests.post(url, data = humair)
        y = requests.post(url, data = humsol)
        z = requests.post(url, data = light)        
    except requests.exceptions.RequestException as e:
        LOG.write_log("error.log", e)
    
    ALARM.blink_light(blue_light)

client = paho.Client()
client.on_message = onMessage

if client.connect("localhost", 1883, 60) != 0:
    print("Error !")
    LOG.write_log("MQTT.log", "An error occured. Can't connect to Broker")
    ALARM.set_light(red_light,green_light)
    sys.exit(-1)

client.subscribe("mqtt/esp32")

try:
    client.loop_forever()
except:
    print("Disconnecting from broker")
    LOG.write_log("error.log", "An error occured. Disconnecting from broker")
    ALARM.set_light(red_light,green_light)