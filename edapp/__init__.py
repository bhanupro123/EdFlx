from tokenize import String
from flask import Flask, render_template,flash
from flask_sqlalchemy import SQLAlchemy
from reg import db
from reg import users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edflx.db'
app.config['SECRET_KEY'] = 'd5997016ea9265b73abe1f59'

db = SQLAlchemy(app)

from edapp import routes