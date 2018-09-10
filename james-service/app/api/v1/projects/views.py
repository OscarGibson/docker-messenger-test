from flask.views import MethodView
from flask import request, send_file
from .forms import ProjectForm, ProjectUpdateForm, ProjectSettingsForm
from .serializers import ProjectSerializer, ProjectSettingsSerializer, ProjectIdSerializer
from .models import Project, ProjectSettings
from helpers.functions.responses import ErrorResponse, SuccessResponse
from helpers.functions.html_converter import HTMLConverter
# from helpers.messages import MESSAGES
from app.api.v1.auth.authenticate import authenticate
from sqlalchemy import exc
# from sqlalchemy.orm import load_only
from app import db
from . import SectionsMessenger, SubSectionsMessenger, IdeasMessenger, SectionsListMessenger
from .messenger import send_message
import requests


# TEST message broker
# from message_broker.producer import send_message

def get_error_message(*responses):
    for response in responses:
        if response.status_code != 201 or response.status_code != 200:
            return True, response.reason
    return False, '<EMPTY>'

class ProjectAPI(MethodView):

    @authenticate
    def get(self, user_data, *args, **kwargs):
        """Get list of user's projects"""
        projects = Project.query.filter_by(user_id= user_data['id'], status= Project.ProjectStatus.ACTIVE)

        output = []

        for project in projects:

            project_json = ProjectSerializer().dump(project)[0]

            if 'include_child' in request.args:

                SubSectionsMessenger.set_headers(request)
                sub_sections_response = SubSectionsMessenger.send(
                    params= '?project_id=%i' % project.id,
                    method= 'get'
                    )

                SectionsMessenger.set_headers(request)
                sections_response = SectionsMessenger.send(
                    params= '&project_id=%i' % project.id,
                    method= 'get'
                    )

                IdeasMessenger.set_headers(request)
                ideas_response = IdeasMessenger.send(
                    params= '?project_id=%i' % project.id,
                    method= 'get'
                    )

                if sub_sections_response.status_code == 200:
                    project_json['sub_sections_count'] = sub_sections_response.json()['data']['sub_sections_count']

                if sections_response.status_code == 200:
                    project_json['words_count'] = sections_response.json()['data']['words_count']
                    project_json['sections_count'] = sections_response.json()['data']['sections_count']

                if ideas_response.status_code == 200:
                    project_json['notes_count'] = len(ideas_response.json()['data'])

            output.append(project_json)

        return SuccessResponse(
            message= "List of user's projects",
            data= output
            # data= sub_sections_response.status_code
            ).data


    @authenticate
    def post(self, user_data):
        """Create project"""
        print('CREATE PROJECT: ', request.get_json())
        form = ProjectForm(**request.get_json())

        if not form.validate():
            return ErrorResponse(
                message= "Invalid payload",
                code= 400
                ).data

        form.user_id.data = user_data['id']
        form.author.data = user_data['name']

        project = Project.create_by_form(form)
        db.session.add(project)
        db.session.commit()

        return SuccessResponse(
            message= "Project #%i created" % project.id,
            data= ProjectSerializer().dump(project)[0],
            code= 201
        ).data

class ExportProjectAPI(MethodView):

    @authenticate
    def get(self, user_data, project_id):

        if 'file_type' not in request.args:
            return ErrorResponse(
                message= "Invalid file type",
                code= 400
                ).data
        file_type = request.args['file_type']

        project = Project.query.filter_by(id= project_id, user_id= user_data['id']).first()
        if not project:
            return ErrorResponse(
                message= "Project not found",
                code= 404
                ).data

        output = ProjectSerializer().dump(project)[0]

        SectionsListMessenger.set_headers(request)
        sections_response = SectionsListMessenger.send(
            params= (project.id, '?include_paragraphs=true')
            )
        if sections_response.status_code == 200:
            output['sections'] = sections_response.json()['data']
        else:
            ErrorResponse(
                message= "Cannot found subsections, original error %s" % str(section_response.reason),
                code= section_response.status_code
                ).data

        html_object = HTMLConverter(output)

        try:
            name, source = html_object.get(request.args['file_type'])
        except Exception as e:
            return ErrorResponse(
                message= "Can't convert data to file, original exception: %s" % str(e)
                ).data

        return send_file(source, as_attachment= True, attachment_filename= f"{name}.{file_type}", cache_timeout= -1)

        # return SuccessResponse(
        #     message= "success",
        #     code= 200,
        #     data= html_object.get_html()
        #     ).data



class SingleProjectAPI(MethodView):

    @authenticate
    def get(self, user_data, project_id):
        """Get user's single project"""

        result = send_message(
            body= {
            'name' : 'Ostap',
            'id'   : 'lalka'
            },
            consumer_name= "user",
            consumer_type= "user",
            )


        project = Project.query.filter_by(id= project_id, user_id= user_data['id']).first()
        if not project:
            return ErrorResponse(
                message= "Project not found",
                code= 404
                ).data

        IdeasMessenger.set_headers(request)
        ideas_response = IdeasMessenger.send(
            method= 'get',
            params= '?project_id=%i' % project.id
            )

        output = ProjectSerializer().dump(project)[0]

        if ideas_response.status_code == 200:
            output['notes'] = ideas_response.json()['data']


        if 'include_sections' in request.args:
            SectionsListMessenger.set_headers(request)
            sections_response = SectionsListMessenger.send(
                params= (project.id, '?include_sub_sections=true&include_notes=true')
                )
            if sections_response.status_code == 200:
                output['sections'] = sections_response.json()['data']
            else:
                output['sections'] = sections_response.status_code

        return SuccessResponse(
            message= "Project #%i for user #%i" % (project_id, user_data['id']),
            data= output
            ).data


    @authenticate
    def put(self, user_data, project_id):
        """Update single project"""
        project = Project.query.filter_by(user_id= user_data['id'], id= project_id, status= Project.ProjectStatus.ACTIVE).first()
        if not project:
            return ErrorResponse(
                message= "Project not found",
                code= 404
                ).data

        if 'deep_copy' not in request.args:

            form = ProjectForm(**request.get_json())

            if not form.validate():
                return ErrorResponse(
                    message= "Invalid payload",
                    code= 403
                    ).data

            project.update_by_form(form)
            db.session.add(project)
            db.session.commit()

            return SuccessResponse(
                message= "Project #%i updated" % project.id,
                data= ProjectSerializer().dump(project)[0],
                code= 201
                ).data
        else:
            new_project = project.copy()
            db.session.commit()

            output = ProjectSerializer().dump(new_project)[0]

            IdeasMessenger.set_headers(request)
            ideas_response = IdeasMessenger.send(
                params= '?project_id=%s&section_id=%i&new_project_id=%s&new_section_id=%i' % (
                    project_id, -1, new_project.id, -1 
                    ),
                method= 'put'
                )

            SectionsMessenger.set_headers(request)
            section_response = SectionsMessenger.send(
                params= '&project_id=%i&new_project_id=%i' % (project.id, new_project.id),
                method= 'put'
                )

            if ideas_response.status_code == 201 and section_response.status_code == 201:
                output['notes'] = ideas_response.json()['data']
                output['sections'] = section_response.json()['data']
                return SuccessResponse(
                    message= "Project copied",
                    data= output,
                    code= 201,
                    ).data
            else:
                output['notes'] = str(ideas_response.reason)
                output['sections'] = str(section_response.reason)
                db.session().rollback()
                # print("RESPONSE: ", section_response.reason)
                return SuccessResponse(**section_response.json()).data

    @authenticate
    def delete(self, user_data, project_id):
        """Delete project"""
        project = Project.query.filter_by(user_id= user_data['id'], id= project_id, status= Project.ProjectStatus.ACTIVE).first()
        if not project:
            return ErrorResponse(
                message= "Project not found",
                code= 404
                ).data

        SubSectionsMessenger.set_headers(request)
        sub_sections_response = SubSectionsMessenger.send(
            params= '?project_id=%i' % project.id,
            method= 'delete'
            )

        IdeasMessenger.set_headers(request)
        ideas_response = IdeasMessenger.send(
            params= '?project_id=%i' % project.id,
            method= 'delete'
            )

        SectionsMessenger.set_headers(request)
        section_response = SectionsMessenger.send(
            params= '&project_id=%i' % project.id,
            method= 'delete'
            )

        have_error, message = get_error_message(sub_sections_response, ideas_response, section_response)

        if have_error:
            return ErrorResponse(
                message= "Error on deleting project, original error: " % message,
                code= 500
                ).data

        project.status = Project.ProjectStatus.DELETED
        db.session.add(project)
        db.session.commit()
        return SuccessResponse(
            message= "Project %i deleted" % project.id,
            code= 201
            ).data

class SettignsProjectAPI(MethodView):

    @authenticate
    def post(self, user_data, project_id):
        """Create project settings"""
        project = Project.query.filter_by(user_id= user_data['id'], id= project_id, status= Project.ProjectStatus.ACTIVE).first()
        if not project:
            return ErrorResponse(
                message= "Project not found",
                code= 404
                ).data

        form = ProjectSettingsForm(**request.get_json())

        if not form.validation():
            return ErrorResponse(
                message= "Invalid payload",
                code= 400
                ).data

        project_settings = ProjectSettings.create(form)
        project.project_settings_id = project_settings.id
        db.session.add(project_settings)
        db.session.add(project)
        db.session.commit()

        return SuccessResponse(
            message= "Project settings created",
            code= 201
            ).data

    @authenticate
    def get(self, user_data, project_id, settings_id, **kwargs):
        """Get project settings"""
        project = Project.query.filter_by(user_id= user_data['id'], id= project_id, status= Project.ProjectStatus.ACTIVE).first()
        if not project:
            return ErrorResponse(
                message= "Project not found",
                code= 404
                ).data

        if project.project_settings_id != settings_id:
            return ErrorResponse(
                message= "Invalid settings id",
                code= 400,
                ).data

        settings = ProjectSettings.query.get(project.id)
        if not settings:
            return ErrorResponse(
                message= "Settings not found",
                code= 404
                ).data

        return SuccessResponse(
            data= ProjectSettingsSerializer().dump(settings)[0],
            message= "Project's #%i settings" % project.id
            ).data


