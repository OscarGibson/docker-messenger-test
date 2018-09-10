from sqlalchemy.exc import IntegrityError

from app import db
from app.api.v1.projects.models import Project, ProjectSettings
from app.api.v1.tests.base import BaseTestCase
from app.api.v1.tests.utils import add_project
import os

class TestProjectModel(BaseTestCase):

    def test_add_project(self):
        project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)
        self.assertTrue(project.id)
        self.assertEqual(project.title, 'AwesomeProj')
        self.assertEqual(project.description, 'my first project')
        self.assertEqual(project.copyright, 'OstapHyba')
        self.assertTrue(project.dedication, '-'*6)
        self.assertTrue(project.created_at)

    def test_change_project_props(self):
        project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)
        project.title = 'New title'
        project.copyright = 'AbyhPatso'
        db.session.add(project)
        db.session.commit()

        self.assertEqual(project.title, 'New title')
        self.assertEqual(project.copyright, 'AbyhPatso')

    def test_check_default_project_settings(self):
        project = add_project('AwesomeProj', 'my first project', 'OstapHyba', '-'*6, self.user)
        project_settings = ProjectSettings.query.get(project.project_settings_id)
        self.assertTrue(project_settings)
        self.assertEqual(project_settings.orientation, project_settings.Orientation.VERTICAL)
        self.assertEqual(project_settings.margin_top, 1)
        self.assertEqual(project_settings.margin_right, 1)
        self.assertEqual(project_settings.margin_bottom, 1)
        self.assertEqual(project_settings.margin_left, 1)
