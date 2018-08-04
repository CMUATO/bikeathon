from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
import json

config = open("config.json").read()
configDict = json.loads(config)
db_url = configDict['db_url']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

SSLify(app) # force https, only when debug is false, breaks on localhost
