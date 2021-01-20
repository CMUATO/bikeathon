import RPi.GPIO as GPIO
import json, threading, time
from datapusher import Rider

hallPin = 3 # Hall effect sensor pin #
GPIO.setmode(GPIO.BOARD)
GPIO.setup(hallPin, GPIO.IN)
count = 0

with open("piconfig.json", "r") as file:
    configjson = file.read()

configDict = json.loads(configjson)
uid = configDict["uid"]
wheel_radius = configDict["wheel_radius"]
distance = configDict["distance"]

# Object Rider defined in datapusher.py #
rider = Rider(uid=uid, wheel_radius=wheel_radius, distance=distance)

try:
    print("Detecting bike cycles...")
    last = 1
    while True:
        # If there is input set last to 1. If there is no input & last == 1, count ++ and set last to 0 #
        # The code is designed as such to avoid multiple counting when the magnet stays in front of the sensors for a long time #
        # As long as the wheel does not turn faster than this code, the count would be accurate #
        if GPIO.input(hallPin):
            last = 1
        else:
            if last == 1:
                count += 1
                print(count)
                # Prevent pushing too frequently, setting a delay #
                if time.time() - rider.last_push > rider.push_delay:
                    rider.last_push = time.time()
                    push = True
                else:
                    push = False
                # Thread so we can keep tracking distance without waiting #
                # Updating rider and mileage information #
                threading.Thread(target=rider.Changer, args=(push,)).start()
            last = 0
finally:
    GPIO.cleanup()
