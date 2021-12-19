import paho.mqtt.client as paho #import the client1
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


blue_light = 21
green_light = 20

ALARM.set_light(green_light,blue_light)

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

    print("Temperature: {}".format(temperature))
    print("Hum-Sol: {}".format(humsol))
    print("Hum-Air: {}".format(humair))
    print("Light: {}".format(light))
    print("-------------------------")

    try:
        w = requests.post(url, headers=headers, data = temperature, verify=False)
        x = requests.post(url, headers=headers, data = humair, verify=False)
        y = requests.post(url, headers=headers, data = humsol, verify=False)
        z = requests.post(url, headers=headers, data = light, verify=False)
	ALARM.blink_light(green_light)
	if w.text != "Accepted":
	    print("Nyoh : {}".format(w.text))
	    ALARM.set_light(blue_light,green_light)
	    LOG.write_log(w, e)
	else:
	    print("Sent!".format(w.text))
	    ALARM.set_light(green_light,blue_light)
			
    except requests.exceptions.RequestException as e:
	LOG.write_log("error.log", e)
	ALARM.blink_light(blue_light)

client = paho.Client()
client.on_message = onMessage

if client.connect("localhost", 1883, 60) != 0:
    LOG.write_log("error.log", "An error occured. Can't connect to Broker")
    ALARM.set_light(blue_light,green_light)
    sys.exit(-1)

client.subscribe("mqtt/esp32")

try:
    client.loop_forever()
except:
    LOG.write_log("error.log", "An error occured. Disconnecting from broker")
    ALARM.set_light(blue_light,green_light)