import stripe, json, atexit

from flask import abort, request, send_file, send_from_directory
from app_manager import db, app
from models import Stats
from gsheets import init_gsheet, fetch_gsheet_total
from venmo_pull import fetch_venmo_balance

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# EB looks for an 'application' callable by default.
application = app

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/sensor', methods=['POST'])
def postBikeData():
    jsonDict = request.get_json()

    # Throw error if data not included
    if ((not jsonDict) or ('distance' not in jsonDict) or
        ('password' not in jsonDict) or ('bikeid' not in jsonDict)):
        return "missing data", 400

    with open("config.json", "r") as file:
        config = file.read()
        configDict = json.loads(config)
        password = configDict['post_password']

    if jsonDict["password"] != password:
        return "incorrect password", 400

    stats = Stats.query.first()

    if (jsonDict['bikeid'] == 1):
        stats.distance1 = jsonDict["distance"]
    elif (jsonDict['bikeid'] == 2):
        stats.distance2 = jsonDict["distance"]
    else:
        return "bad bikeid", 400

    stats.distance = stats.distance1 + stats.distance2

    db.session.add(stats)
    db.session.commit()

    return 'ok', 200

@app.route("/stats", methods=["GET"])
def getStats():
    stats = Stats.query.first()
    results = {
        "distance": round(stats.distance, 2),
        "money": "%.2f" % (stats.cash + stats.venmo + stats.card + stats.misc),
        "card": stats.card, "venmo": stats.venmo,
        "cash": stats.cash, "misc": stats.misc
    }
    return json.dumps(results), 200

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
        return json.dumps(result), 400

    if amount < 100:
        result = {
            "success" : 0,
            "message" : 'Donation amount must be at least $1'
        }
        return json.dumps(result), 400

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
        stats = Stats.query.first()
        stats.card += amount / 100
        db.session.add(stats)
        db.session.commit()
        return json.dumps(result), 200

    except stripe.error.CardError as e:
        body = e.json_body
        err  = body.get('error', {})
        result = {
            "success" : 0,
            "message" : err.get('message')
        }
        return json.dumps(result), 400

    except Exception as e:
        result = {
            "success" : 0,
            "message" : "An error occurred"
        }
        return json.dumps(result), 400


def stripeSetup():
    # Set your secret key:
    # remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    with open("config.json") as file:
        config = file.read()
        configDict = json.loads(config)
        stripe.api_key = configDict['stripe_api_key']

def initScheduler():
    # Initialize scheduler for updating money from gsheet and venmo
    wks = init_gsheet()
    def updateMoney():
        stats = Stats.query.first()
        stats.cash, stats.misc = fetch_gsheet_total(wks)
        bal = fetch_venmo_balance()
        if bal is not None:
            # None means the token has expired
            stats.venmo = bal - stats.start_venmo_bal
        db.session.add(stats)
        db.session.commit()

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=updateMoney,
        trigger=IntervalTrigger(seconds=10),
        id='money',
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
