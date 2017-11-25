from flask import Flask, abort, request, render_template, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import stripe
import json
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from db_manager import db, app
from gsheets import init_gsheet, fetch_gsheet_total

# Make this an actual database
DATABASE = {
    "distance" : 0,
    "cash_venmo" : 0,
    "cards" : 0
}

#Get speed and distance reading
@app.route('/sensor', methods=['POST'])
def postBikeData():
    jsonDict = request.get_json()
    print(jsonDict)
    #Throw error if data not included
    if ((not jsonDict) or ('speed' not in jsonDict) or
        ('distance' not in jsonDict) or ('bikeid' not in jsonDict)):
        abort(400)

    DATABASE["distance"] += jsonDict["distance"]

    print("SPEED", jsonDict['speed'], "DISTANCE",
          jsonDict['distance'], "BIKE_ID", jsonDict['bikeid'])
    return 'ok', 200

#Get stats
@app.route("/stats", methods=["GET"])
def getDistance():
    results = {
        "distance" : round(DATABASE["distance"], 2),
        "money" : "%.2f" % (DATABASE["cash_venmo"] + DATABASE["cards"])
    }
    return json.dumps(results), 200

#Return index.html
@app.route('/')
def index():
    return send_file('index.html')

# Static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#Charge user
@app.route('/charge-ajax', methods=['POST'])
def charge():
    amount = request.form["amount"] # already in cents
    token = request.form["token"]

    try:
        amount = int(amount)
    except Exception as e:
        result = {
            "success" : 0,
            "message" : 'Please enter a valid amount'
        }
        return json.dumps(result), 200

    if amount < 100:
        result = {
            "success" : 0,
            "message" : 'Donation amount must be at least $1'
        }
        return json.dumps(result), 200

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            source=token,
            description='ATO Bike-A-Thon donation'
        )
        result = {
            "success" : 1,
            "message" : ""
        }
        DATABASE["cards"] += amount / 100
        return json.dumps(result), 200
    except stripe.error.CardError as e:
        body = e.json_body
        err  = body.get('error', {})
        result = {
            "success" : 0,
            "message" : err.get('message')
        }
        return json.dumps(result), 200
    except Exception as e:
        result = {
            "success" : 0,
            "message" : "An error occurred"
        }
        return json.dumps(result), 200


#Set up Stripe
def stripeSetup():
    # Set your secret key:
    # remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    config = open("config.json").read()
    configDict = json.loads(config)
    stripe.api_key = configDict['stripe_api_key']

# Initialize scheduler for updating money from gsheet
def initScheduler():
    # wks = init_gsheet()
    def updateMoney():
        print("Uncomment lines")
        # DATABASE["cash_venmo"] = fetch_gsheet_total(wks) / 100
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=updateMoney,
        trigger=IntervalTrigger(seconds=10),
        id='gsheets',
        name='Update cash and venmo total from gsheet',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

@app.before_first_request
def init():
    stripeSetup()
    initScheduler()

    
if __name__ == '__main__':
    app.run(debug=True)
