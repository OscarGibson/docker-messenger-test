from .views import AuthAPI, ForgotPasswordAPI, RestorePasswordAPI, CheckUserTokenAPI
from helpers.functions.url_rules import UrlRules
from app.api.v1.auth.views import AuthAPI

def add_rules():
	auth_api = AuthAPI.as_view('auth')

	url_rules = UrlRules.create_rules_object('/api/v1')

	url_rules.add('/auth/login', view_func= auth_api, methods= ['POST',])
	url_rules.add('/auth/logout', view_func= auth_api, methods= ['GET',])

	url_rules.add('/auth/forgot_password', view_func= ForgotPasswordAPI.as_view('forgot_password'), methods= ['POST',])
	url_rules.add('/auth/forgot_password_confirmation', view_func= RestorePasswordAPI.as_view('restore_password'), methods= ['POST',])

	url_rules.add('/auth/check-auth', view_func= CheckUserTokenAPI.as_view('check_auth'), methods= ['GET',])