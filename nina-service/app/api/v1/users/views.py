from flask.views import MethodView
from flask import request
from .models import User
from helpers.functions. responses import ErrorResponse, SuccessResponse
from app import db
from app.message_broker.producer import send_message
from app.message_broker.storage import Storage
import time

class UserAPI(MethodView):

    def get(self):
        """_|_|_|_|_|_|_|_|_|_|_|_"""

        start_time = time.time()

        uuid = send_message('james', {
            'key' : 'value'
        })

        while True:
            if Storage.have_message(uuid):
                response = Storage.get_message(uuid)
                return SuccessResponse(
                    data= response
                ).data
            if time.time() - start_time > 30:
                return ErrorResponse(
                    message= "Timeout error",
                    code= 504
                ).data

        return User.query.all().count()
