from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#Set up SQL app
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


#Sensor Data Point
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    speed = db.Column(db.Integer, primary_key=True)


#User database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    distance = db.Column(db.Integer, primary_key=True)
    school= db.Column(db.String(120), unique = True, nullable = False)
    def __repr__(self):
        return '<User %r>' % self.username
