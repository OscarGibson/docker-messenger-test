# manage.py


import unittest
import coverage

from flask_script import Manager
from flask_migrate import MigrateCommand

from app.api.v1.projects.models import Project, ProjectSettings

from app import create_app, db


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/api/v1/tests/*'
    ]
)
COV.start()

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('app/api/v1/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('app/api/v1/tests')
    result = unittest.TextTestRunner(verbosity= 2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    """Seeds the database."""

    project_settings = ProjectSettings()
    db.session.add(project_settings)
    db.session.commit()
    project = Project(
        title= 'My Title',
        description= 'My description',
        copyright= 'OstapHybaInc2018',
        dedication= '-'*6,
        user_id= 999,
        project_settings_id= project_settings.id,
        author= 'Ostap Hyba',
        )
    db.session.add(project)
    db.session.commit()
    project.id = 999
    db.session.add(project)
    db.session.commit()

@manager.command
def list_routes():
    import urllib
    from flask import url_for
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        output.append(line)
    
    for line in sorted(output):
        print(line)




if __name__ == '__main__':
    print('In main')
    manager.run()
    print('After main')
