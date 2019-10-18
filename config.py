import os, json

try:
    config = open("config.json").read()
    configDict = json.loads(config)
    email = configDict["MAIL_USERNAME"]
    mailpass = configDict["MAIL_PASSWORD"]
    postpass = configDict["POST_PASSWORD"]
    venmotok = configDict["VENMO_TOKEN"]
    stripekey = configDict["STRIPE_API_KEY"]
    gsheetskey = configDict["GSHEETS_KEY"]
except FileNotFoundError:
    email = mailpass = postpass = venmotok = stripekey = gsheetskey = None

DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.getenv("MAIL_USERNAME", email)
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", mailpass)
MAIL_DEFAULT_SENDER = MAIL_USERNAME
POST_PASSWORD = os.getenv("POST_PASSWORD", postpass)
VENMO_TOKEN = os.getenv("VENMO_TOKEN", venmotok)
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", stripekey)
GSHEETS_KEY = os.getenv("GSHEETS_KEY", gsheetskey)
