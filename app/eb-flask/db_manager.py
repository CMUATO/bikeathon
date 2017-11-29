from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import json


config = open("config.json").read()
configDict = json.loads(config)
db_url = configDict['db_url']


#Set up SQL app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
