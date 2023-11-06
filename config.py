# This file is located at /config.py

class Config:
    # Secret key for session handling, you can generate random bytes for this
    SECRET_KEY = 'your_secret_key_here'

    # URI for the database. SQLite database file is located at the absolute path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/ukped/OneDrive - RTC Education Ltd/Desktop/loadify/instance/users.db'

    # SQLAlchemy setting to turn off modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directory for file uploads
    UPLOAD_FOLDER = 'static/uploads'
