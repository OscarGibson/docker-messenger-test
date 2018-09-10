from wtforms import Form, StringField, IntegerField, validators
from datetime import datetime

class UserForm(Form):
	name = StringField('Name', [validators.Optional()])
	email = StringField('Email address', [
		validators.Required(),
		validators.Email()
		])
	password = StringField('Password', [validators.Required(), validators.Length(min= 1)])
	photo_url = StringField('Photo url', [])
	photo_name = StringField('Photo url', [])


class UserUpdateForm(Form):
	name = StringField('FirstName', [validators.Length(min= 1), validators.Optional()])
	email = StringField('Email address', [validators.Email(), validators.Optional()])
	password = StringField('Password', [validators.Optional(),])
	old_password = StringField('Old Password', [validators.Optional(),])
	photo_url = StringField('Photo url', [])
	photo_name = StringField('Photo url', [])

class PaymentForm(Form):
	card_number = StringField('Card Number', [validators.Length(min= 16, max= 19), validators.Required()])
	exp_month = IntegerField('Expiration month', [validators.Required(), validators.NumberRange(min= 1, max= 12)])
	exp_year = IntegerField('Expiration year', [validators.Required()])
	cvv = StringField('Cvv code', [validators.Required(), validators.Length(min= 3, max= 4)])
	card_type = StringField('Type', [validators.Required()])

	def validate_date(self):
		if self.validate():
			now = datetime.utcnow()
			if not ((self.exp_month.data < now.month and self.exp_year.data <= now.year) or self.exp_year.data < now.year):
				return True
		return False