import datetime
from enum import Enum
from app import db


class Project(db.Model):

    class ProjectStatus(Enum):
        ACTIVE = 'Active'
        DELETED = 'Deleted'
        PENDING = 'Pending'

    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    title = db.Column(db.String(128), nullable= False)
    description = db.Column(db.String(512), nullable= True)
    copyright = db.Column(db.String(128), nullable= True)
    dedication = db.Column(db.String(128), nullable= True)

    color = db.Column(db.String(128), nullable= True, default= "#fafafa")
    thumbnail_url = db.Column(db.String(128), nullable= True)
    thumbnail_name = db.Column(db.String(128), nullable= True)

    status = db.Column(db.Enum(ProjectStatus))
    author = db.Column(db.String(257), nullable= True)
    created_at = db.Column(db.DateTime, nullable= True)
    updated_at = db.Column(db.DateTime, nullable= True)

    user_id = db.Column(db.Integer, nullable= False)
    project_settings_id = db.Column(db.Integer, nullable= True)

    @property
    def status_value(self):
        return self.status.value

    class Meta:
        updatable_fields = ('title', 'description', 'copyright', 'dedication', 'thumbnail_url', 'thumbnail_name')

    def __init__(
            self, title, description, copyright, dedication, user_id, project_settings_id, author,
            status= ProjectStatus.ACTIVE,
            created_at= datetime.datetime.utcnow(), updated_at= datetime.datetime.utcnow()):

        self.title = title
        self.description = description
        self.copyright = copyright
        self.dedication = dedication
        self.status = status
        self.author = author

        self.created_at = created_at
        self.updated_at = updated_at

        self.user_id = user_id
        self.project_settings_id = project_settings_id

    def update_fields(self, **fields):
        for field_name, value in fields.items():
            setattr(self, field_name, value)
        self.updated_at = datetime.datetime.utcnow()

    def copy(self):

        project_settings = ProjectSettings.query.get(self.project_settings_id)
        if project_settings:
            new_project_settings = ProjectSettings(
                orientation= project_settings.orientation,
                margin_top= project_settings.margin_top,
                margin_right= project_settings.margin_right,
                margin_bottom= project_settings.margin_bottom,
                margin_left= project_settings.margin_left
                )
        else:
            new_project_settings = ProjectSettings()
        db.session.add(new_project_settings)
        db.session.commit()

        new_project = self.__class__(
            title= self.title,
            description= self.description,
            copyright= self.copyright,
            dedication= self.dedication,
            user_id= self.user_id,
            author= self.author,
            project_settings_id= new_project_settings.id
            )
        db.session.add(new_project)
        return new_project

    @staticmethod
    def create_by_form(form):
        project_settings = ProjectSettings()
        db.session.add(project_settings)
        db.session.commit()
        return Project(
            title= form.title.data,
            description= form.description.data,
            copyright= form.copyright.data,
            dedication= form.dedication.data,
            author= form.author.data,
            user_id= form.user_id.data,
            project_settings_id= project_settings.id
            )

    def update_by_form(self, form):
        fields = {}
        for field in Project.Meta.updatable_fields:
            fields[field] = getattr(form, field).data
        self.update_fields(**fields)



class ProjectSettings(db.Model):

    class Orientation(Enum):
        HORIZONTAL = 'horizontal'
        VERTICAL = 'vertical'
        
    __tablename__ = "projects_settings"
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    orientation = db.Column(db.Enum(Orientation))
    margin_top = db.Column(db.Float, default= 1)
    margin_right = db.Column(db.Float, default= 1)
    margin_bottom = db.Column(db.Float, default= 1)
    margin_left = db.Column(db.Float, default= 1)

    @property
    def orientation_value(self):
        return self.orientation.value

    def __init__(self, orientation= Orientation.VERTICAL, margin_top= 1,
                    margin_right= 1, margin_bottom= 1, margin_left= 1):

        self.orientation = orientation
        self.margin_top = margin_top
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left

    def create(self, form):
        self(
            orientation= form.orientation.data,
            margin_top= form.margin_top.data,
            margin_right= form.margin_right.data,
            margin_bottom= form.margin_bottom.data,
            margin_left= form.margin_left.data,
            )











