from app import db
from flask_login import UserMixin
import datetime

class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    images = db.relationship('Image', backref='user', lazy=True)
    admin = db.Column(db.Boolean, nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_type = db.Column(db.String(50), nullable=False)  # person/cloth
    image_path = db.Column(db.String(300), nullable=False)
