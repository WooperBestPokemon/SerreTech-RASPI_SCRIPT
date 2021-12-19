import RPi.GPIO as GPIO
import requests
import time
import sys
import LOG
import yaml
import json

with open("config.yaml", "r") as yalm_data:
    config_data = yaml.safe_load(yalm_data)

zone = config_data["zone_id"]
url = "{}{}".format(config_data["address_water"],zone)
token = config_data["token"]

headers={'Authorization': "Bearer {}".format(token)}

try:
    x = requests.get(url, headers=headers, verify=False)
    result = json.loads(x.text)
    #If it doesn't throw an error, it check if we need to add water
    if result["water"] == 0:
        output = []
        #Calculating the number of seconds
        seconds = float(result["quantity"]) / 30

        #Starting the pump and letting out the water
        GPIO.setmode(GPIO.BCM)
        RELAIS_1_GPIO = 26
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
        output.append("[+] The pump will be running for {} seconds...".format(seconds))
        
        #In seconds, this is the time the pump will be running
        time.sleep(seconds)
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
        output.append("[-] the pump has been shutdown.")
        LOG.write_log("pump_output.log", output)
        
except requests.exceptions.RequestException as e:
    LOG.write_log("error_pump.log", e)