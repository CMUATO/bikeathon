from app_manager import db

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Float, nullable=False)
    cash = db.Column(db.Float, nullable=False)
    venmo = db.Column(db.Float, nullable=False)
    card = db.Column(db.Float, nullable=False)
    misc = db.Column(db.Float, nullable=False)
    start_venmo_bal = db.Column(db.Float, nullable=False)

    # Riders can be nullable, if no one is on them
    # Init is None for riders
    # rider1 = db.Column(db.String(50), nullable=True)
    # rider2 = db.Column(db.String(50), nullable=True)

    # Give dummy values to init these
    leader = db.Column(db.String(50), nullable=False)
    school_leader = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Stats %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    school = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return '<User %r>' % self.name
