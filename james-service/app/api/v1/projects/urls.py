from .views import ProjectAPI, SingleProjectAPI, SettignsProjectAPI, ExportProjectAPI
from helpers.functions.url_rules import UrlRules

def add_rules():
	projects_api = ProjectAPI.as_view('projects')
	project_api = SingleProjectAPI.as_view('project')
	settings_api = SettignsProjectAPI.as_view('settings')
	export_api = ExportProjectAPI.as_view('export')

	url_rules = UrlRules.create_rules_object('/api/v1')

	url_rules.add('/projects', view_func= projects_api, methods= ['POST', 'GET'])

	url_rules.add('/projects/<int:project_id>', view_func= project_api, methods= ['GET', 'PUT', 'DELETE'])

	url_rules.add('/projects/<int:project_id>/export', view_func= export_api, methods= ['GET',])

	url_rules.add('/projects/<int:project_id>/settings', view_func= settings_api, methods= ['POST',])
	url_rules.add('/projects/<int:project_id>/settings/<int:settings_id>', view_func= settings_api, methods= ['GET', 'PUT'])