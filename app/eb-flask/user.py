from db_manager import db


#User database model
class User(db.Model):
    name = db.Column(db.String(50), unique=True, nullable=False,
                     primary_key=True)
    distance = db.Column(db.Integer, nullable=False)
    school = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return '<User %r>' % self.name
