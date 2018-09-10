import datetime
from app import db
from app.api.v1.projects.models import Project, ProjectSettings


def add_project(title, description, copyright, dedication, user):
    project_settings = ProjectSettings()
    db.session.add(project_settings)
    db.session.commit()
    project = Project(
        title= title,
        description= description,
        copyright= copyright,
        dedication= dedication,
        user_id= user.id,
        project_settings_id= project_settings.id,
        author= user.first_name + ' ' + user.last_name,
        )
    db.session.add(project)
    db.session.commit()
    return project