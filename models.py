# This file is located at /models.py

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# User model
class User(db.Model, UserMixin):
    # User ID
    id = db.Column(db.Integer, primary_key=True)
    # Username
    username = db.Column(db.String(150), nullable=False, unique=True)
    # Password (hashed)
    password = db.Column(db.String(150), nullable=False)

    # Method to set the user's password (hashes the password)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Method to check if a password matches the user's password
    def check_password(self, password):
        return check_password_hash(self.password, password)