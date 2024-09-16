import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_really_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://cloth_project:trycatch@localhost/cloth_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
