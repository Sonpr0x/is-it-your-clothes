# This module hold init config.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from gradio_client import Client, handle_file



# db = SQLAlchemy()


# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_really_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://cloth_project:trycatch@localhost/cloth_project'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    #db.init_app(app)
    #db.create_all()
    from app.controllers import main_bp

    return app

app = create_app()

if __name__ == '__main__':
    # public
    # app.run(debug=True, host='0.0.0.0', port=5000)

    # local
    app.run(debug=True, host='0.0.0.0', port=5000)