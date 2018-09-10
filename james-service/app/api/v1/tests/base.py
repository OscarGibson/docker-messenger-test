from flask_testing import TestCase

from app import create_app, db

class BaseTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.create_app()
        self.user = BaseTestCase.User(
            self.app.config['TEST_USER_FIRST_NAME'],
            self.app.config['TEST_USER_LAST_NAME'],
            self.app.config['TEST_USER_EMAIL'],
            self.app.config['TEST_USER_PASSWORD'],
            self.app.config['TEST_USER_ID'],
            )

    class User:
        def __init__(self, first_name, last_name, email, password, id):
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
            self.password = password
            self.id = id

    def create_app(self):
        self.app = create_app('testing')
        return self.app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
