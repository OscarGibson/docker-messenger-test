# project/tests/test_user_model.py


from sqlalchemy.exc import IntegrityError

from app import db
from app.api.v1.users.models import User
from app.api.v1.tests.base import BaseTestCase
from app.api.v1.tests.utils import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('justatest', 'yeah', 'test@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.first_name, 'justatest')
        self.assertEqual(user.last_name, 'yeah')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.created_at)
        self.assertTrue(user.admin == False)

    def test_encode_auth_token(self):
        user = add_user('justatest', 'yeah', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('justatest', 'yeah', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'yeah', 'test@test.com', 'test')
        duplicate_user = User(
            first_name= 'justatest2',
            last_name= 'yeah',
            email= 'test@test.com',
            password= 'test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('justatest', 'yeah', 'test@test.com', 'test')
        user_two = add_user('justatest2', 'yeah2', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)
