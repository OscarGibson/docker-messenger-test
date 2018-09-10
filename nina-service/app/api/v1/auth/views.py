from flask.views import MethodView
from flask import request
from .forms import LoginForm, ForgotPasswordForm, RestorePasswordForm
from app.api.v1.users.models import User, ConfirmationCode
from app.api.v1.auth.authenticate import authenticate
from app.api.v1.users.serializers import UserSerializer

from app import db, bcrypt

from helpers.functions.responses import ErrorResponse, SuccessResponse
from helpers.messages import MESSAGES

class AuthAPI(MethodView):

    #login
    def post(self):
        # login user, return auth_token
        form = LoginForm(**request.get_json())

        if not form.validate():
            return ErrorResponse(
                message= MESSAGES.INVALID_PAYLOAD,
                code= 400
                ).data

        try:
            user = User.query.filter_by(email= form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return SuccessResponse(
                        message= MESSAGES.SUCCESS_LOGIN,
                        auth_token= auth_token.decode(),
                        user_id = user.id,
                        created_at= user.created_at
                        ).data

                else:
                    return ErrorResponse(
                        message= MESSAGES.USER_NOT_EXIST,
                        code= 404
                        ).data

            else:
                return ErrorResponse(
                    message= MESSAGES.INVALID_UNAME_OR_PASS,
                    code= 403
                    ).data
        except Exception as e:
            user = User.query.filter_by(email= form.email.data).first()
            return ErrorResponse(
                message= MESSAGES.TRY_AGAIN,
                ).data

    #logout
    @authenticate
    def get(self, auth_user_id):
        try:
            user = User.query.get(auth_user_id)
            auth_token = user.encode_auth_token(auth_user_id)
            if auth_token:
                return SuccessResponse(
                    message= MESSAGES.SUCCESS_LOGOUT,
                    auth_token= auth_token.decode()
                    ).data
        except Exception as e:
            pass
        else:
            return ErrorResponse(
                message= MESSAGES.CANT_LOGOUT,
                code= 403
                ).data


class ForgotPasswordAPI(MethodView):

    def post(self):
        """Get email to send confirmation code"""
        form = ForgotPasswordForm(**request.get_json())

        response_object = ErrorResponse(
            message= MESSAGES.INVALID_PAYLOAD,
            code= 403
            )

        if not form.validate():
            return response_object.data

        user = User.query.filter_by(email= form.email.data).first()

        if not user:
            response_object.message = MESSAGES.INVALID_EMAIL
            return response_object.data    

        # create confirm code
        confirmation_code = ConfirmationCode(user_id= user.id)
        db.session.add(confirmation_code)
        db.session.commit()

        user.send_conformation_code(form.email.data, confirmation_code.code)

        return SuccessResponse(
            message= MESSAGES.CODE_SENDED
            ).data



class RestorePasswordAPI(MethodView):


    def post(self):
        """Check if confirmation code exist, update password"""
        form = RestorePasswordForm(**request.get_json())

        response_object = ErrorResponse(
            message= MESSAGES.INVALID_PAYLOAD,
            code= 400
            )

        if not form.validate():
            return response_object.data

        confirmation_code = ConfirmationCode.query.filter_by(code= form.code.data).first()
        if not confirmation_code:
            response_object.message = MESSAGES.INVALID_CODE
            response_object.code = 401
            return response_object.data

        if confirmation_code.activated:
            response_object.message = MESSAGES.CODE_ACTIVATED
            response_object.code = 401
            return response_object.data

        confirmation_code.activated = True
        confirmation_code.save()
        user = User.query.get(confirmation_code.user_id)
        user.update_password(form.password.data)
        user.save()
        return SuccessResponse(
            message= MESSAGES.SUCCESS_PASS_CHANGE
            ).data


class CheckUserTokenAPI(MethodView):

    def get(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return ErrorResponse(
                message= MESSAGES.INVALID_TOKEN,
                code= 403
                ).data

        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)

        if isinstance(resp, str):
            return ErrorResponse(
                message= resp,
                code= 403
                ).data

        user = User.query.filter_by(id= resp).first()
        if not user:
            return ErrorResponse(
                message= MESSAGES.SOMETHING_WRONG,
                code= 401
                ).data

        return SuccessResponse(
            message= "Success",
            data= UserSerializer().dump(user)[0]
            ).data














