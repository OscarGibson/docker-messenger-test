from .views import UserAPI
from helpers.functions.url_rules import UrlRules


def add_rules():
	url_rules = UrlRules.create_rules_object('/nina')

	url_rules.add('/nina-test', view_func= UserAPI.as_view('users'), methods= ['GET',])
