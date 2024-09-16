from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @staticmethod
    def validate_login(username, password):
        user = User.query.filter_by(username=username, password=password).first()
        return user is not None

