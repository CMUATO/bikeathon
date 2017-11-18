from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#Set up SQL app
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
