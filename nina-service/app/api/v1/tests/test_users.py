# app/tests/test_users.py


import json
import datetime

from app import db
from app.api.v1.users.models import User
from app.api.v1.tests.base import BaseTestCase
from app.api.v1.tests.utils import add_user

BASE_URL = '/api/v1/%s'

url = lambda path: BASE_URL % path


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('michael', 'user', 'michael@realpython.com', 'test')

        resp_login = self.client.post(
                url('auth/login'),
                data=json.dumps(dict(
                    email='michael@realpython.com',
                    password='test'
                )),
                content_type='application/json'
            )


        with self.client:
            response = self.client.get(url(f'users/{user.id}'),
                headers=dict(
                    Authorization='JWT ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('michael', data['data']['first_name'])
            self.assertIn('user', data['data']['last_name'])
            self.assertIn('michael@realpython.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        user = add_user('michael', 'user', 'michael@realpython.com', 'test')
        resp_login = self.client.post(
                url('auth/login'),
                data=json.dumps(dict(
                    email='michael@realpython.com',
                    password='test'
                )),
                content_type='application/json'
            )
        with self.client:
            response = self.client.get(url('users/blah'),
                headers=dict(
                    Authorization='JWT ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            # data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            # self.assertIn('User does not exist', data['message'])
            # self.assertIn('error', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        user = add_user('michael', 'user', 'michael@realpython.com', 'test')
        resp_login = self.client.post(
                url('auth/login'),
                data=json.dumps(dict(
                    email='michael@realpython.com',
                    password='test'
                )),
                content_type='application/json'
            )
        with self.client:
            response = self.client.get(url('users/999'),
                headers=dict(
                    Authorization='JWT ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('error', data['status'])

