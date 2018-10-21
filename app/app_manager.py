from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_sslify import SSLify
import json

config = open("config.json").read()
configDict = json.loads(config)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = configDict["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = configDict["MAIL_SERVER"]
app.config["MAIL_PORT"] = configDict["MAIL_PORT"]
app.config["MAIL_USE_SSL"] = configDict["MAIL_USE_SSL"]
mail_username = configDict["MAIL_USERNAME"]
app.config["MAIL_USERNAME"] = mail_username
app.config["MAIL_PASSWORD"] = configDict["MAIL_PASSWORD"]
app.config["MAIL_DEFAULT_SENDER"] = mail_username

db = SQLAlchemy(app)

mail = Mail(app)

SSLify(app) # force https, only when debug is false, breaks on localhost
