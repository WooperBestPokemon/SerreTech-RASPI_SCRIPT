import RPi.GPIO as GPIO
import requests
import time
import sys
import LOG

url = 'http://localhost:8000/api/water'

try:
    x = requests.get(url)
    result = json.loads(x.text)
    #If it doesn't throw an error, it check if we need to add water
    if result["water"]:
        output = []
        #Calculating the number of seconds
        seconds = float(result["quantity"]) / 30

        #Starting the pump and letting out the water
        GPIO.setmode(GPIO.BCM)
        RELAIS_1_GPIO = 20
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
        output.append("[+] The pump will be running for {} seconds...".format(seconds))
        
        #In seconds, this is the time the pump will be running
        time.sleep(seconds)
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
        output.append("[-] the pump has been shutdown.")
        LOG.write_log("pump.log", output)
        
except requests.exceptions.RequestException as e:
    print("Server not found !")
    LOG.write_log("error.log", e)
