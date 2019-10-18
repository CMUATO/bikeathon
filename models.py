from app_manager import db

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Float, nullable=False)
    distance1 = db.Column(db.Float, nullable=False)
    distance2 = db.Column(db.Float, nullable=False)
    cash = db.Column(db.Float, nullable=False)
    venmo = db.Column(db.Float, nullable=False)
    card = db.Column(db.Float, nullable=False)
    misc = db.Column(db.Float, nullable=False)
    start_venmo_bal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Stats %r>' % self.id
