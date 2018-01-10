import stripe, json, atexit

from flask import abort, request, send_file, send_from_directory
from flask_sslify import SSLify

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from db_manager import db, app
# from user import User
from stats import Stats

from gsheets import init_gsheet, fetch_gsheet_total
from venmo_pull import fetch_venmo_balance

# EB looks for an 'application' callable by default.
application = app

# For https redirecting, only happens when debug=False
# Doesn't work on localhost
# sslify = SSLify(app)

#Get speed and distance reading
@app.route('/sensor', methods=['POST'])
def postBikeData():
    jsonDict = request.get_json()
    print(jsonDict)
    #Throw error if data not included
    if ((not jsonDict) or ('speed' not in jsonDict) or
        ('distance' not in jsonDict) or ('bikeid' not in jsonDict)):
        abort(400)

    stats = db.session.query(Stats).first()

    stats.distance += jsonDict["distance"]

    # Not sure what the bikeid's are, change if not 1 and 2
    # if (jsonDict['bikeid'] == 1) and (stats.rider1 is not None):
    #     User.query.get(stats.rider1).distance += jsonDict["distance"]
    # if (jsonDict['bikeid'] == 2) and (stats.rider2 is not None):
    #     User.query.get(stats.rider1).distance += jsonDict["distance"]

    db.session.commit()
    db.session.close()

    print("SPEED", jsonDict['speed'], "DISTANCE",
          jsonDict['distance'], "BIKE_ID", jsonDict['bikeid'])
    return 'ok', 200

#Get stats
@app.route("/stats", methods=["GET"])
def getStats():
    stats = db.session.query(Stats).first()
    results = {
        "distance": round(stats.distance, 2),
        "money": "%.2f" % (stats.cash + stats.venmo + stats.card + stats.misc),
        "card": stats.card, "venmo": stats.venmo,
        "cash": stats.cash, "misc": stats.misc
    }
    db.session.close()
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
        stats = db.session.query(Stats).first()
        stats.card += amount / 100
        db.session.commit()
        db.session.close()
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
        stats = db.session.query(Stats).first()
        stats.cash, stats.misc = fetch_gsheet_total(wks)
        bal = fetch_venmo_balance()
        if bal is not None:
            # None means the token has expired
            stats.venmo = bal - stats.start_venmo_bal
        db.session.commit()
        db.session.close()

    # schools = {'CMU': 0, 'CIT': 0, 'SCS': 0, 'HSS': 0,
    #            'TSB': 0, 'MCS': 0, 'CFA': 0}
    # def updateLeaders():
    #     stats = db.session.query(Stats).first()
    #     leader = None
    #     lead = 0
    #     for user in db.session.query(User).all():
    #         if user.distance > lead:
    #             leader = user.name
    #             lead = user.distance
    #         schools[user.school] += user.distance
    #     school_leader = None
    #     school_lead = 0
    #     for school in schools:
    #         if schools[school] > school_lead:
    #             school_leader = school
    #     if leader is not None:
    #         stats.leader = leader
    #     if school_leader is not None:
    #         stats.school_leader = school_leader
    #     db.session.commit()
    #     db.session.close()

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=updateMoney,
        trigger=IntervalTrigger(seconds=10),
        id='money',
        name='Update cash and venmo totals',
        replace_existing=True)
    # scheduler.add_job(
    #     func=updateLeaders,
    #     trigger=IntervalTrigger(seconds=10),
    #     id='leaders',
    #     name='Update leaders in distance',
    #     replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    updateMoney()
    # updateLeaders()

@app.before_first_request
def init():
    stripeSetup()
    initScheduler()

if __name__ == '__main__':
    app.run(debug=False)
