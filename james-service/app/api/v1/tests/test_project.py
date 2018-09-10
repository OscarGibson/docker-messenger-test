import json
import datetime

from app import db
from app.api.v1.projects.models import Project
from app.api.v1.tests.base import BaseTestCase
from app.api.v1.tests.utils import add_project
import requests

BASE_URL = '/api/v1/%s'
USER_URL = 'http://users-service:5000/api/v1/%s'

url = lambda path: BASE_URL % path

user_url = lambda path: USER_URL % path


class TestProjectService(BaseTestCase):
    """Tests for the Users Service."""

    def test_single_project(self):
        """Ensure get single project behaves correctly."""
        project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)

        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)
        response = self.client.get(url(f'projects/{project.id}'),
            headers= dict(
                Authorization='JWT ' + resp_login.json()['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('created_at' in data['data'])
        self.assertIn('AwesomeProj', data['data']['title'])
        self.assertIn('my first project', data['data']['description'])
        self.assertIn('OstapHyba', data['data']['copyright'])
        self.assertIn('-'*6, data['data']['dedication'])
        self.assertIn(Project.ProjectStatus.ACTIVE.value, data['data']['status_value'])
        self.assertIn('Ostap Hyba', data['data']['author'])
        self.assertTrue(data['data']['created_at'])
        self.assertIn('success', data['status'])

    def test_single_project_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)
        
        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)
        response = self.client.get(url(f'projects/iuhi'),
            headers= dict(
                Authorization='JWT ' + resp_login.json()['auth_token']
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_single_project_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)
        
        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                )
            )

        self.assertEqual(resp_login.status_code, 200)
        response = self.client.get(url(f'projects/09808'),
            headers= dict(
                Authorization='JWT ' + resp_login.json()['auth_token']
            )
        )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn('Project not found', data['message'])
        self.assertIn('error', data['status'])

    def test_create_project(self):
        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)
        with self.client:
            response = self.client.post(url('projects'),
                headers= dict(
                    Authorization='JWT ' + resp_login.json()['auth_token']
                ),
                data= json.dumps(dict(
                    title= 'Title 1',
                    description= 'some description',
                    copyright= 'OstapHybaInc2018',
                    dedication= '-'*12
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

            self.assertTrue('id' in data['data'])

            created_project = Project.query.get(data['data']['id'])

            self.assertEqual(created_project.title, data['data']['title'])
            self.assertEqual(created_project.title, 'Title 1')

            self.assertEqual(created_project.description, data['data']['description'])
            self.assertEqual(created_project.description, 'some description')

            self.assertEqual(created_project.copyright, data['data']['copyright'])
            self.assertEqual(created_project.copyright, 'OstapHybaInc2018')

            self.assertEqual(created_project.dedication, data['data']['dedication'])
            self.assertEqual(created_project.dedication, '-'*12)

            self.assertEqual(created_project.status_value, data['data']['status_value'])
            self.assertEqual(created_project.status_value, Project.ProjectStatus.ACTIVE.value)

            self.assertEqual(created_project.author, data['data']['author'])
            self.assertEqual(created_project.author, self.user.first_name + ' ' + self.user.last_name)

            self.assertTrue(data['data']['created_at'])

    def test_create_project_no_title(self):
        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)

        with self.client:
            response = self.client.post(url(f'projects'),
                headers= dict(
                    Authorization='JWT ' + resp_login.json()['auth_token']
                ),
                data= json.dumps(dict(
                    description= 'some description',
                    copyright= 'OstapHybaInc2018',
                    dedication= '-'*12
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)

    def test_create_project_no_description(self):
        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)

        with self.client:
            response = self.client.post(url(f'projects'),
                headers= dict(
                    Authorization='JWT ' + resp_login.json()['auth_token']
                ),
                data= json.dumps(dict(
                    title= "empty title",
                    copyright= 'OstapHybaInc2018',
                    dedication= '-'*12
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)

    def test_create_project_no_copyright(self):
        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)

        with self.client:
            response = self.client.post(url(f'projects'),
                headers= dict(
                    Authorization='JWT ' + resp_login.json()['auth_token']
                ),
                data= json.dumps(dict(
                    title= "123123",
                    description= 'some description',
                    dedication= '-'*12
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)

    def test_create_project_no_dedication(self):
        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)

        with self.client:
            response = self.client.post(url(f'projects'),
                headers= dict(
                    Authorization='JWT ' + resp_login.json()['auth_token']
                ),
                data= json.dumps(dict(
                    title= "---",
                    description= 'some description',
                    copyright= 'OstapHybaInc2018',
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)

    def test_update_project_all_fields(self):

        created_project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)

        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)

        with self.client:
            response_update = self.client.put(url(f'projects/{created_project.id}'),
                headers= dict(
                    Authorization='JWT ' + resp_login.json()['auth_token']
                ),
                data= json.dumps(dict(
                    title= 'Title 2',
                    description= 'some description 2',
                    copyright= 'OstapHybaInc2018 2',
                    dedication= '-'*10
                )),
                content_type='application/json'
            )

            self.assertEqual(created_project.title, 'Title 2')
            self.assertEqual(created_project.description, 'some description 2')
            self.assertEqual(created_project.copyright, 'OstapHybaInc2018 2')
            self.assertEqual(created_project.dedication, '-'*10)
            self.assertEqual(created_project.status_value, Project.ProjectStatus.ACTIVE.value)
            self.assertEqual(created_project.author, self.user.first_name + ' ' + self.user.last_name)

    def test_delete_project(self):
        project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)

        resp_login = requests.post(
                user_url('auth/login'),
                json= dict(
                    email= self.user.email,
                    password= self.user.password
                ),
            )

        self.assertEqual(resp_login.status_code, 200)

        with self.client:
            response = self.client.delete(url(f'projects/{project.id}'),
                headers= dict(
                    Authorization='JWT ' + resp_login.json()['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(f'Project {project.id} deleted', data['message'])
            deleted_project = Project.query.filter_by(user_id= self.user.id, id= project.id, status= Project.ProjectStatus.DELETED).first()
            self.assertTrue(deleted_project)





















