from db_manager import db

#Sensor Data Point
class SensorData(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.Integer, primary_key=True)
	speed = db.Column(db.Integer, primary_key=True)