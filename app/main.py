from flask import Flask, abort, request, render_template, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import stripe
import json
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from db_manager import db, app
from user import User
from stats import Stats

from gsheets import init_gsheet, fetch_gsheet_total
from venmo_pull import fetch_venmo_balance


if __name__ == '__main__':
    # Here temporarily since the db is stored in memory currently
    import init_db
    stats = Stats.query.first()


#Get speed and distance reading
@app.route('/sensor', methods=['POST'])
def postBikeData():
    jsonDict = request.get_json()
    print(jsonDict)
    #Throw error if data not included
    if ((not jsonDict) or ('speed' not in jsonDict) or
        ('distance' not in jsonDict) or ('bikeid' not in jsonDict)):
        abort(400)

    stats.distance += jsonDict["distance"]

    print("SPEED", jsonDict['speed'], "DISTANCE",
          jsonDict['distance'], "BIKE_ID", jsonDict['bikeid'])
    return 'ok', 200

#Get stats
@app.route("/stats", methods=["GET"])
def getStats():
    results = {
        "distance" : round(stats.distance, 2),
        "money" : "%.2f" % (stats.cash + stats.venmo + stats.card)
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
        stats.card += amount / 100
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

# Initialize scheduler for updating money from gsheet and venmo
def initScheduler():
    wks = init_gsheet()
    def updateMoney():
        stats.cash = fetch_gsheet_total(wks)
        stats.venmo = fetch_venmo_balance() - stats.start_venmo_bal
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=updateMoney,
        trigger=IntervalTrigger(seconds=10),
        id='gsheets',
        name='Update cash and venmo totals',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    updateMoney()

@app.before_first_request
def init():
    stripeSetup()
    initScheduler()

    
if __name__ == '__main__':
    app.run(debug=True)
