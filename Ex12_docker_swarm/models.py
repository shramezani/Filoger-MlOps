from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    predictions = db.relationship("PredictionHistory", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    area = db.Column(db.Float, nullable=False)  # Area in square meters
    rooms = db.Column(db.Integer, nullable=False)  # Number of rooms
    parking = db.Column(db.Boolean, nullable=False)  # Parking: True/False
    warehouse = db.Column(db.Boolean, nullable=False)  # Warehouse: True/False
    elevator = db.Column(db.Boolean, nullable=False)  # Elevator: True/False
    address = db.Column(db.Text, nullable=True)  # Address as text
    predicted_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
