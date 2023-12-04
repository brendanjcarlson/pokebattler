from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_APP = environ.get('FLASK_APP') 
    FLASK_DEBUG = True if environ.get('FLASK_DEBUG') == "True" else False 

    SECRET_KEY = environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True if environ.get('FLASK_DEBUG') == "True" else False
