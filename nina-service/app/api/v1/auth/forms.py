from wtforms import Form, StringField, validators

class LoginForm(Form):
	email = StringField('Login', [
		validators.Required(),
		validators.Email()
		])
	password = StringField('Password', [validators.Required()])

class ForgotPasswordForm(Form):
	email = StringField('Email address', [
		validators.Email()
		])

class RestorePasswordForm(Form):
	code = StringField('Confirmation code', [
		validators.Required(),
		])
	password = StringField('New password', [
		validators.Required(),
		])