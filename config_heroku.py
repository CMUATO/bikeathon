import subprocess, json

config = open("config.json").read()
configDict = json.loads(config)
email = configDict["MAIL_USERNAME"]
mailpass = configDict["MAIL_PASSWORD"]
postpass = configDict["POST_PASSWORD"]
venmotok = configDict["VENMO_TOKEN"]
stripekey = configDict["STRIPE_API_KEY"]
gsheetskey = configDict["GSHEETS_KEY"]

subprocess.run(["heroku", "config:set",
    "MAIL_USERNAME=" + email,
    "MAIL_PASSWORD=" + mailpass,
    "POST_PASSWORD=" + postpass,
    "VENMO_TOKEN=" + venmotok,
    "STRIPE_API_KEY=" + stripekey,
    "GSHEETS_KEY=" + gsheetskey],
    shell=True)
