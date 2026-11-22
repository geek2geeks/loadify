# This file is located at /config.py

import os


class Config:
    # Secret key for session handling. Set the SECRET_KEY environment variable
    # in CI/production; the fallback is a development placeholder only.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')

    # URI for the database. Relative SQLite paths are resolved by
    # Flask-SQLAlchemy against the app instance folder, so this maps to
    # instance/users.db on every machine and OS.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///users.db')

    # SQLAlchemy setting to turn off modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directory for file uploads
    UPLOAD_FOLDER = 'static/uploads'
