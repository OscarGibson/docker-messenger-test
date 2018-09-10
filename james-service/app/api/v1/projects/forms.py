from wtforms import Form, StringField, FloatField, validators

class ProjectForm(Form):
    title = StringField('Title', [validators.Length(min= 1)])
    description = StringField('Description', [])
    copyright = StringField('Copyright', [validators.DataRequired()])
    dedication = StringField('Dedicated', [validators.DataRequired()])
    user_id = StringField('UserId', [])
    author = StringField('Author', [])
    color = StringField('Color', [])
    thumbnail_url = StringField('Thumbnail url', [])
    thumbnail_name = StringField('Thumbnail name', [])


class ProjectUpdateForm(Form):
    title = StringField('Title', [validators.Length(min= 1)])
    description = StringField('Description', [])
    copyright = StringField('Copyright', [])
    dedication = StringField('Dedicated', [])
    user_id = StringField('UserId', [])
    author = StringField('Author', [])
    color = StringField('Color', [])
    thumbnail_url = StringField('Thumbnail url', [])
    thumbnail_name = StringField('Thumbnail name', [])

class ProjectSettingsForm(Form):
    orientation = StringField('Orientation', [])
    margin_top = FloatField('Margin top', [])
    margin_right = FloatField('Margin right', [])
    margin_bottom = FloatField('Margin bottom', [])
    margin_left = FloatField('Margin left', [])