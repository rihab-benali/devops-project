from . import db


# Role table
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

# User table with role_id
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship("Role", backref="users")
