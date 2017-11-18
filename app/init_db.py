from db_manager import db
from user import User


db.create_all()


users = [User(username='grant', school='cit'),
         User(username='cchris', school='hss'),
         User(username='brandon', school='scs'),
         User(username='daniel', school='scs')]


for user in users:
    db.session.add(user)

db.session.commit()
