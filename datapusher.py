import time, math, requests, json

class Rider(object):
    def __init__(self, uid, wheel_radius, distance=0):
        """Wheel radius in inches"""
        self.uid = uid

        in_to_mil = 0.000015783
        radius = wheel_radius * in_to_mil
        self.circumference = 2 * math.pi * radius

        config = open("app/config.json").read()
        configDict = json.loads(config)
        url = configDict["url"]
        password = configDict["post_password"]
        self.url = "%s/sensor" % url
        self.password = password

        self.distance = distance
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
        print("Pushing...")
        headers = {"content-type": "application/json"}
        r = requests.post(self.url, data=json.dumps(self.payload),
            headers=headers)
        print(r)
        self.last_push = time.time()

        with open("piconfig.json", "r") as file:
            configjson = file.read()
            configDict = json.loads(configjson)
            configDict["distance"] = self.distance
            configjson = json.dumps(configDict, indent=4, sort_keys=True)

        with open("piconfig.json", "w") as file:
            file.write(configjson)

    def Changer(self):
        """Add distance to payload"""
        self.Update_Payload()
        if time.time() - self.last_push > self.push_delay:
            self.Push()
