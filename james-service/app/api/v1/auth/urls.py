from .check_auth import CheckAuth
from helpers.functions.url_rules import UrlRules

def add_rules():
	url_rules = UrlRules.create_rules_object('/api/v1')
	url_rules.add('/projects/check-auth', view_func= CheckAuth.as_view('check_auth_iuhoiu'), methods= ['POST',])