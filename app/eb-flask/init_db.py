from db_manager import db
from user import User
from stats import Stats

from venmo_pull import fetch_venmo_balance

import sys


def init_db():
    db.create_all()


    bal = fetch_venmo_balance()
    if bal is None:
        print('fetch_venmo_balance returned None. Please reauthorize to fetch '
              'initial venmo balance.')
        sys.exit("Database initialization failed.")

    db.session.add(Stats(distance=0,
                         cash=0,
                         venmo=0,
                         card=0,
                         misc=0,
                         start_venmo_bal=bal,
                         leader='No one',
                         school_leader='CMU'))


    # Uses txt file 'user_list.txt'
    # Format as follows:
    # My Name,SCS
    # Other Name,CIT
    # Another Person,HSS
    # Guest,CMU
    # ...
    with open('user_list.txt', 'r') as f:
        text = f.read()

    for line in text.splitlines():
        items = line.split(',')
        assert len(items) == 2
        db.session.add(User(name=items[0], school=items[1], distance=0))


    db.session.commit()


if __name__ == '__main__':
    init_db()
