from db_manager import db


#User database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    school= db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return '<User %r>' % self.name
