import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql://cloth_project:trycatch@localhost/myappdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
