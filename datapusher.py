import time
import math
import requests
import random

class Rider(object):
	#name should be string
	#NEED TO ADD URL TO BOTTOM
	def __init__(self, name="Cool Chris", wheel_radius = 25, Thresold = 5000, push_delay = 5):
		self.name = name
		self.last_time = time.time()
		self.time_change = 0
		self.wheel_radius = wheel_radius
		self.circumfrence = 2*math.pi*self.wheel_radius
		self.currently_hi = True
		self.Thresold = Thresold
		self.last_speed = 0
		self.url = "https://facebook.com"
		self.payload = {"name":self.name, "speed":self.last_speed, "time":time.time()}
		self.distance = 0
		self.last_push = time.time()
		self.push_delay = push_delay

	#Returns the amount of time since last cycle
	#Updates the time of the Rider
	def Time_elapsed(self):
		holder = self.last_time
		self.last_time = time.time()
		self.time_change = self.last_time - holder
		return self.time_change

	#We caculate speed it must of
	#roatated for a full cycle
	def Speed(self):
		self.last_speed = float(self.circumfrence)/self.Time_elapsed()

	#Updates speed to make sure accurate for payload
	def Update_Payload(self):
		self.Speed()
		self.distance += self.circumfrence
		self.payload = {"name":self.name, "distance":self.distance, "spped":self.last_speed,"time":time.time()}


	#Sends payload to server at url
	#sends name and speed as variables
	def Push(self):
		r = requests.post(self.url, data=self.payload)
		self.last_push = time.time()
		self.distance = 0;

	#Looks to see if data is freshly over data
	#If is then sends speed of the average speed of wheel over
	#Last rotation
	def Changer(self):
		if(time.time() - self.last_time >= .1):
			self.Update_Payload()
		#if(time.time() - self.last_push>self.push_delay):
			#self.Push()





	








