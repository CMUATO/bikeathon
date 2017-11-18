from db_manager import db
from user import User


db.create_all()


# Currently fails if school is not unique
users = [User(username='grant', school='cit'),
         User(username='cchris', school='hss'),
         User(username='brandon', school='scs'),
         User(username='daniel', school='mcs')]


for user in users:
    db.session.add(user)

db.session.commit()
