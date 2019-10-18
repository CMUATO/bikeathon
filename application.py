import re, stripe, json, atexit, os

from flask import request, render_template, send_file
from flask_mail import Message

from app_manager import db, app, mail
from models import Stats
from gsheets import init_gsheet, fetch_gsheet_total
from venmo_pull import fetch_venmo_balance

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

@app.route("/")
def index():
    return ""
    return send_file("templates/index.html")

@app.route("/sensor", methods=["POST"])
def postBikeData():
    jsonDict = request.get_json()

    # Throw error if data not included
    if ((not jsonDict) or ("distance" not in jsonDict) or
        ("password" not in jsonDict) or ("bikeid" not in jsonDict)):
        return "missing data", 400

    password = app.config["POST_PASSWORD"]

    if jsonDict["password"] != password:
        return "incorrect password", 400

    stats = Stats.query.first()

    # set the distance to the new total
    if (jsonDict["bikeid"] == 1):
        stats.distance1 = jsonDict["distance"]
    elif (jsonDict["bikeid"] == 2):
        stats.distance2 = jsonDict["distance"]
    else:
        return "bad bikeid", 400

    stats.distance = stats.distance1 + stats.distance2

    db.session.add(stats)
    db.session.commit()

    return "ok", 200

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
    name = censor(request.form["donor"][:30])
    email = validate_email(request.form["email"])

    try:
        amount = int(amount)
    except Exception as e:
        result = {
            "success" : 0,
            "message" : "Please enter a valid amount"
        }
        return json.dumps(result), 400

    if amount < 100:
        result = {
            "success" : 0,
            "message" : "Donation amount must be at least $1"
        }
        return json.dumps(result), 400

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,
            description="ATO Bike-A-Thon donation"
        )
        result = {
            "success" : 1,
            "message" : ""
        }

        if email is not None:
            subject = "Thank you for donating"
            html = render_template("email.html", name=name, amount=amount/100)
            send_email(email, subject, html)

        stats = Stats.query.first()
        stats.card += amount / 100
        db.session.add(stats)
        db.session.commit()
        return json.dumps(result), 200

    except stripe.error.CardError as e:
        body = e.json_body
        err  = body.get("error", {})
        result = {
            "success" : 0,
            "message" : err.get("message")
        }
        return json.dumps(result), 400

    except Exception as e:
        result = {
            "success" : 0,
            "message" : "An error occurred"
        }
        return json.dumps(result), 400

email_pattern = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
email_regex = re.compile(email_pattern, re.IGNORECASE)
def validate_email(text):
    match = email_regex.match(text.strip())
    if match is not None:
        return match.group(0)
    return None

def make_censorer():
    txt = os.getenv("CENSOR_TEXT", "bad").strip().lower()
    words = txt.splitlines()
    pattern = "|".join([re.escape(word) for word in words])
    pattern = r"\b(?:%s)\b" % pattern
    return re.compile(pattern)

censorer = make_censorer()

def censor(text):
    return censorer.sub("", text)

def send_email(email, subject, html):
    msg = Message(subject, recipients=[email], html=html)
    mail.send(msg)

def stripeSetup():
    # Set your secret key:
    # remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = app.config["STRIPE_API_KEY"]

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
        id="money",
        name="Update cash and venmo totals",
        replace_existing=True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    updateMoney()

@app.before_first_request
def init():
    stripeSetup()
    initScheduler()

if __name__ == "__main__":
    app.run(debug=True)
