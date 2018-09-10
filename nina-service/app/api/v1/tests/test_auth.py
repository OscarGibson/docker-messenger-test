# project/tests/test_auth.py


import json
import time


from app import db
from app.api.v1.users.models import User
from app.api.v1.tests.base import BaseTestCase
from app.api.v1.tests.utils import add_user

BASE_URL = '/api/v1/%s'

url = lambda path: BASE_URL % path

class TestAuthBlueprint(BaseTestCase):

    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                url('users'),
                data=json.dumps(dict(
                    first_name= 'Test',
                    last_name= 'Unit',
                    email= 'test@test.com',
                    password= '123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        add_user('Test', 'Duplicated', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                url('users'),
                data=json.dumps(dict(
                    first_name= 'who',
                    last_name= 'are_you',
                    email= 'test@test.com',
                    password= 'test'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                url('users'),
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('first_name: This field is required.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_firstname(self):
        with self.client:
            response = self.client.post(
                url('users'),
                data=json.dumps(dict(email= 'test@test.com', password= 'test', last_name= 'Lastname')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('first_name: This field is required.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_lastname(self):
        with self.client:
            response = self.client.post(
                url('users'),
                data=json.dumps(dict(email= 'test@test.com', password= 'test', first_name= 'Firstname')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('last_name: This field is required.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                url('users'),
                data=json.dumps(dict(
                    first_name='justatest', last_name= 'Lastname', password='test')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            print('EMAIL: ', data['message'])
            self.assertIn('email: This field is required.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                url('users'),
                data=json.dumps(dict(
                    first_name='justatest', last_name= 'Lastname', email='test@test.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('This field is required.', data['message'])
            self.assertIn('error', data['status'])

    def test_registered_user_login(self):
        with self.client:
            add_user('test', 'user', 'test@test.com', 'test')
            response = self.client.post(
                url('auth/login'),
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                url('auth/login'),
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Invalid user name and password')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_valid_logout(self):
        add_user('test', 'user', 'test@test.com', 'test')
        with self.client:
            # user login
            resp_login = self.client.post(
                url('auth/login'),
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            # valid token logout
            response = self.client.get(
                url('auth/logout'),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                url('auth/logout'),
                headers=dict(Authorization='Bearer invalid'))

            data = json.loads(response.data.decode('utf-8'))
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 403)

