from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import stripe


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    distance = db.Column(db.Integer, primary_key=True)
    school= db.Column(db.String(120), unique = True, nullable = False)
    def __repr__(self):
        return '<User %r>' % self.username

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

# Token is created using Checkout or Elements!
# Get the payment token ID submitted by the form:
stripe.Charge.retrieve(
  "ch_1BKZ5Q2eZvKYlo2CrmTJgJBF",
  api_key="sk_test_BQokikJOvBiI2HlWgH4olfQ2"
)