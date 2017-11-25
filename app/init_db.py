from db_manager import db
from user import User
from stats import Stats

from venmo_pull import fetch_venmo_balance


db.create_all()


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


db.session.add(Stats(distance=0,
                     cash=0,
                     venmo=0,
                     card=0,
                     start_venmo_bal=fetch_venmo_balance(),
                     leader='No one',
                     school_leader='CMU'))


db.session.commit()
