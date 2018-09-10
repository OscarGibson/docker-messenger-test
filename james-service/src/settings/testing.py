from .base import *
import os

DEBUG = True
TESTING = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')

TEST_USER_FIRST_NAME = 'Ostap'
TEST_USER_LAST_NAME = 'Hyba'
TEST_USER_EMAIL = 'oneostap@gmail.com'
TEST_USER_PASSWORD = 'password'
TEST_USER_ID = 999