from flask import db


class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username =  db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.Integer(), nullable=False, unique=True)
    role = db.Column(db.String(), nullable=False, unique=False)