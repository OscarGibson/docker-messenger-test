from flask.views import MethodView
from flask import request
from helpers.functions.responses import ErrorResponse, SuccessResponse
from app.api.v1.auth.authenticate import authenticate
from app.api.v1.projects.models import Project
from sqlalchemy import exc
from app import db

class CheckAuth(MethodView):

    @authenticate
    def post(self, user_data):
        project_id = request.get_json()['project_id']

        project = Project.query.filter_by(id= project_id, user_id= user_data['id'], status= Project.ProjectStatus.ACTIVE).first()
        if not project or (project_id != project.id):
            return ErrorResponse(code= 404).data
        return SuccessResponse().data
