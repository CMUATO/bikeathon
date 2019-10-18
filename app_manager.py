from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_sslify import SSLify

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

mail = Mail(app)

SSLify(app) # force https, only when debug is false, breaks on localhost
