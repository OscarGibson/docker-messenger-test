from helpers.functions.responses import ErrorResponse, SuccessResponse
from helpers.messages import MESSAGES
from flask import request
from app.api.v1.users.models import User
from functools import wraps

def authenticate(f):
    @wraps(f)
    def decorated_function(obj, *args, **kwargs):
        response_object = {
            'status': 'error',
            'message': 'Something went wrong. Please contact us.'
        }
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

        return f(obj, resp, *args, **kwargs)
    return decorated_function