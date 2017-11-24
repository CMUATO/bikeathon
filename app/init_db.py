from db_manager import db
from user import User


db.create_all()


with open('user_list.txt', 'r') as f:
    text = f.read()


for line in text.splitlines():
    items = line.split(',')
    db.session.add(User(name=items[0], school=items[1], distance=0))


db.session.commit()
