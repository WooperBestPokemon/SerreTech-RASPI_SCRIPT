import RPi.GPIO as GPIO
import time
import sys
import LOG

def add_water(millimeter):
	output = []
	#Calculating the number of seconds
	seconds = float(millimeter) / 30

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
