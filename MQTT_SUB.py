import paho.mqtt.client as paho
from datetime import datetime
import requests
import sys
import time
import json
import LOG
import ALARM
import yaml

with open("config.yaml", "r") as yalm_data:
    config_data = yaml.load(yalm_data)

url = config_data["address_post"]
token = config_data["token"]

headers={'Authorization': "Bearer {}".format(token)}

temp_sensor = config_data["temp_sensor"]
solhum_sensor = config_data["solhum_sensor"]
airhum_sensor = config_data["airhum_sensor"]
light_sensor = config_data["light_sensor"]


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

    temperature = {'data' : p.temperature, 'sensor' : temp_sensor}
	humsol = {'data' : p.humsol, 'sensor' : solhum_sensor}
    humair = {'data' : p.humair, 'sensor' : airhum_sensor}
    light = {'data' : p.light, 'sensor' : light_sensor}
    
    try:
        w = requests.post(url, headers=headers, data = temperature)
        x = requests.post(url, headers=headers, data = humair)
        y = requests.post(url, headers=headers, data = humsol)
        z = requests.post(url, headers=headers, data = light)
		ALARM.blink_light(blue_light)
		if w.text != "Accepted":
			ALARM.set_light(red_light,green_light)
			LOG.write_log("error_MQTT.log", w)
		else:
			ALARM.set_light(green_light,red_light)
			
    except requests.exceptions.RequestException as e:
        LOG.write_log("error_MQTT.log", e)
		ALARM.blink_light(red_light)

client = paho.Client()
client.on_message = onMessage

if client.connect("localhost", 1883, 60) != 0:
    LOG.write_log("error_MQTT.log", 'An error occured. Can\'t connect to Broker')
    ALARM.set_light(red_light,green_light)
    sys.exit(-1)

client.subscribe("mqtt/esp32")

try:
    client.loop_forever()
except:
    LOG.write_log("error_MQTT.log", 'An error occured. Disconnecting from broker')
    ALARM.set_light(red_light,green_light)