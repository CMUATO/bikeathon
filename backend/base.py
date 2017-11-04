from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    distance = db.Column(db.Integer, primary_key=True)
    school= db.Column(db.String(120), unique = True, nullable = False)
    donation = db.relationship('donation', backref='user', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.username


class donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
