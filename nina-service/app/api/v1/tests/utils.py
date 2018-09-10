# project/tests/utils.py


import datetime


from app import db
from app.api.v1.users.models import User


def add_user(first_name, last_name, email, password, created_at= datetime.datetime.utcnow()):
    user = User(
        first_name= first_name,
        last_name= last_name,
        email= email,
        password= password,
        created_at= created_at)
    db.session.add(user)
    db.session.commit()
    return user
