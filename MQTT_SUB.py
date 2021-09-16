import paho.mqtt.client as paho #import the client1
from datetime import datetime
import mysql.connector
import sys
import time
import json
import LOG
import ALARM

red_light = 17
green_light = 18

ALARM.set_light(green_light,red_light)

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

#Execute onMessage every time it gets a message
def sendDataDB(query):
    mydb = mysql.connector.connect(
       host="185.201.11.212",
       user="u882331052_projet",
       password="Cegep2021",
       database="u882331052_projet"
    )
    mycursor = mydb.cursor()
    mycursor.execute(query)
    mydb.commit()

def onMessage(client, userdata, msg):
    
    j = msg.payload.decode()
    p = Payload(j)
    print("-------- {} --------".format(datetime.now()))
    print("id: {}".format(p.id))
    print("temperature: {} celcius".format(p.temperature))
    print("Air Humidity: {}%".format(p.humair))
    print("Ground Humidity: {}%".format(p.humsol))
    print("Luminosity : {} lux".format(p.light))
    print("")
    print("Full string: {}".format(j))
    print("")
	
    sendDataDB("INSERT INTO tblTest (data, typeData, idSensor) VALUES ({},'Temperature',{})".format(p.temperature, p.id))
    sendDataDB("INSERT INTO tblTest (data, typeData, idSensor) VALUES ({},'Air Humidity',{})".format(p.humair, p.id))
    sendDataDB("INSERT INTO tblTest (data, typeData, idSensor) VALUES ({},'Ground Humidity',{})".format(p.humsol, p.id))
    sendDataDB("INSERT INTO tblTest (data, typeData, idSensor) VALUES ({},'Luminosity',{})".format(p.light, p.id))
    ALARM.blink_light(27)

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
    LOG.write_log("MQTT.log", "An error occured. Disconnecting from broker")
    ALARM.set_light(red_light,green_light)
