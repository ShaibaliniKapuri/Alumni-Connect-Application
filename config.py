import os

class Config:
    SECRET_KEY = 'bootcamp_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alumni.db'
    SQLALCHEMY_TRACK_MODIFICATION = False
    UPLOAD_FOLDER = os.path.join('static','uploads')
    MAX_UPLOAD_LENGTH = 16*1024*1024

