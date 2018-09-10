# project/tests/base.py


from flask_testing import TestCase

from app import create_app, db

app = create_app('testing')


class BaseTestCase(TestCase):

    # current_app = app

    def create_app(self):
        # self.current_app = create_app()
        # app.config.from_object('src.settings.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
