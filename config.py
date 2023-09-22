import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    FLASK_APP = os.environ.get('FLASK_APP') or "app"
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 0
    SECRET_KEY = os.environ.get('SECRET_KEY') or "1234"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
