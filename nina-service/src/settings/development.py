from .base import *
import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
BCRYPT_LOG_ROUNDS = 4

# email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'testlviv9@gmail.com'
MAIL_PASSWORD = 'userincora'
MAIL_USE_TLS = False
MAIL_USE_SSL = True