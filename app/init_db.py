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
# It's Me,CIT
# ...
with open('user_list.txt', 'r') as f:
    text = f.read()

for line in text.splitlines():
    items = line.split(',')
    assert len(items) == 2
    db.session.add(User(name=items[0], school=items[1], distance=0))


bal = fetch_venmo_balance()
db.session.add(Stats(distance=0, cash=0, venmo=0, card=0, start_venmo_bal=bal))


db.session.commit()
