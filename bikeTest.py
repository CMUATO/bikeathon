#!/usr/bin/env python2.7
# demo of "BOTH" bi-directional edge detection
# script by Alex Eames http://RasPi.tv
# http://raspi.tv/?p=6791

import RPi.GPIO as GPIO
from time import sleep     # this lets us have a time delay (see line 12)
from datetime import datetime
from datapusher import Rider

hallPin = 17
prevTime = datetime.now()

GPIO.setmode(GPIO.BCM)
GPIO.setup(hallPin, GPIO.IN) 
count = 0

rider = Rider()


def detectCycle(channel):
	global prevTime
	global count

	currTime = datetime.now()
	deltaTime = currTime - prevTime
	# if (deltaTime.total_seconds() * 1000) >= 100:
	# 	count += 1
	# 	print count
	# 	prevTime = currTime
	rider.Changer()

GPIO.add_event_detect(hallPin, GPIO.FALLING, callback=detectCycle)  


try:  
    print "Detecting bike cycles."
    while True:
  		pass
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  