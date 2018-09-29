from app_manager import db
from models import Stats
from venmo_pull import fetch_venmo_balance
import sys

def init_db():
    db.drop_all()
    print("woah")
    db.create_all()
    print("nelly")

    bal = fetch_venmo_balance()
    if bal is None:
        print("fetch_venmo_balance returned None. Please reauthorize to fetch "
              "initial venmo balance.")
        sys.exit("Database initialization failed.")

    print("fuck")
    db.session.add(Stats(distance=0,
                         distance1=0,
                         distance2=0,
                         cash=0,
                         venmo=0,
                         card=0,
                         misc=0,
                         start_venmo_bal=bal))
    print("me")
    db.session.commit()

if __name__ == '__main__':
    init_db()
