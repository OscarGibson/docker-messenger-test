import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        self.app = create_app('development')
        return self.app

    def test_app_is_development(self):
        self.assertTrue(
            self.app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )

class TestTestingConfig(TestCase):
    def create_app(self):
        self.app = create_app('testing')
        return self.app

    def test_app_is_testing(self):
        print('LOCAL: %s' % self.app.config['SECRET_KEY'])
        print('GLOBAL: %s' % os.environ.get('SECRET_KEY'))
        self.assertTrue(
            self.app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(self.app.config['TESTING'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )

class TestProductionConfig(TestCase):
    def create_app(self):
        self.app = create_app('production')
        return self.app

    def test_app_is_production(self):
        self.assertTrue(
            self.app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertFalse(self.app.config['DEBUG'])
        self.assertFalse(self.app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
