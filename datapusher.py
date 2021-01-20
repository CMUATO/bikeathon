import time, math, requests, json

# Defining rider object used in other files #
class Rider(object):
    def __init__(self, uid, wheel_radius, distance=0):
        """Wheel radius in inches"""
        self.uid = uid

        # inches to miles #
        in_to_mil = 0.000015783
        radius = wheel_radius * in_to_mil
        self.circumference = 2 * math.pi * radius

        config = open("config.json").read()
        configDict = json.loads(config)
        url = configDict["URL"]
        password = configDict["POST_PASSWORD"]
        self.url = "%s/sensor" % url
        self.password = password

        self.distance = distance
        # Payload is the update package to server #
        self.payload = dict(bikeid=self.uid,
                            distance=self.distance,
                            password=self.password)
        self.last_push = time.time()
        self.push_delay = 5

    def Update_Payload(self):
        """Add circumference to distance and update payload"""
        self.distance += self.circumference
        self.payload["distance"] = self.distance

    def Push(self):
        """Sends payload to server at url and updates local json"""
        with open("piconfig.json", "r") as file:
            configjson = file.read()

        configDict = json.loads(configjson)
        # Update local json with the up to date distance info #
        # I think this code is implicitly assuming there is one rider #
        # To add more riders, we need to be careful with editting dictionary #
        configDict["distance"] = self.distance
        configjson = json.dumps(configDict, indent=4, sort_keys=True)

        # Commit changes #
        with open("piconfig.json", "w") as file:
            file.write(configjson)

        print("Pushing...")
        headers = {"content-type": "application/json"}
        
        # Push commend on the side of Raspberry Pi #
        r = requests.post(self.url, data=json.dumps(self.payload),
            headers=headers, timeout=3)
        print(r)

    # Changer function used in sensor.py #
    def Changer(self, push):
        """Add distance to payload"""
        self.Update_Payload()
        if push:
            self.Push()
