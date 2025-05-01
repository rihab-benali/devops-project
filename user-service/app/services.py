'''from .models import User
from . import db

def get_all_users():
    return [ {"id": u.id, "name": u.name, "email": u.email} for u in User.query.all() ]

def create_user(data):
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return {"id": user.id, "name": user.name}'''
