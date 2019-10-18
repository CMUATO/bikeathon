import os, json

try:
    config = open("config.json").read()
    configDict = json.loads(config)
    email = configDict["MAIL_USERNAME"]
    password = configDict["MAIL_PASSWORD"]
except FileNotFoundError:
    email = password = None

DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.getenv("MAIL_USERNAME", email)
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", password)
MAIL_DEFAULT_SENDER = MAIL_USERNAME
