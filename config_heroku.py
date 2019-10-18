import subprocess, json

config = open("config.json").read()
configDict = json.loads(config)
email = configDict["MAIL_USERNAME"]
password = configDict["MAIL_PASSWORD"]

subprocess.run(["heroku", "config:set",
    "MAIL_USERNAME=" + email,
    "MAIL_PASSWORD=" + password],
    shell=True)
