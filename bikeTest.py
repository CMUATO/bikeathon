#!/usr/bin/env python2.7
# demo of "BOTH" bi-directional edge detection
# script by Alex Eames http://RasPi.tv
# http://raspi.tv/?p=6791

import RPi.GPIO as GPIO
from time import sleep     # this lets us have a time delay (see line 12)

hallPin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(hallPin, GPIO.IN) 


def detectCycle(channel):
	print "Magnet detected"

GPIO.add_event_detect(hallPin, GPIO.FALLING, callback=detectCycle)  



try:  
    print "Detecting bike cycles."
    while True:
  		pass
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  