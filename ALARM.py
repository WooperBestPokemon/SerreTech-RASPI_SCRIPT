import RPi.GPIO as GPIO
import time

def set_light(pin_turn_on, pin_turn_off):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin_turn_on,GPIO.OUT)
    GPIO.output(pin_turn_on,GPIO.HIGH)
    GPIO.setup(pin_turn_off,GPIO.OUT)
    GPIO.output(pin_turn_off,GPIO.LOW)
	
def blink_light(pin_number):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin_number,GPIO.OUT)
    GPIO.output(pin_number,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.setup(pin_number,GPIO.OUT)
    GPIO.output(pin_number,GPIO.LOW)
