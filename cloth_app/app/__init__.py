from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    #db.create_all()
    from app.controllers import main_bp
    app.register_blueprint(main_bp)

    return app
