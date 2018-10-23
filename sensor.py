import RPi.GPIO as GPIO
import json, threading
from datapusher import Rider

hallPin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(hallPin, GPIO.IN)
count = 0

with open("piconfig.json", "r") as file:
    configjson = file.read()
    configDict = json.loads(configjson)
    uid = configDict["uid"]
    wheel_radius = configDict["wheel_radius"]
    distance = configDict["distance"]

rider = Rider(uid=uid, wheel_radius=wheel_radius, distance=distance)

try:
    print("Detecting bike cycles...")
    last = 1
    while True:
        if GPIO.input(hallPin):
            last = 1
        else:
            if last == 1:
                count += 1
                print(count)
                # thread so we can keep tracking distance without waiting
                threading.Thread(target=rider.Changer).start()
            last = 0
finally:
    GPIO.cleanup()
