from flask.views import MethodView
from flask import request
from .models import User
from helpers.functions. responses import ErrorResponse, SuccessResponse
from app import db, message_broker
# from app.message_broker.producer import send_message
# from app.message_broker.storage import Storage
import app

class UserAPI(MethodView):

    def get(self):
        """_|_|_|_|_|_|_|_|_|_|_|_"""


        answer = message_broker.send_and_wait(
            receiver_name= "james",
            question= {
                'method_name': 'mult_numbers',
                'kwargs' : {
                    'x' : 1,
                    'y' : 2,
                }
            }
            )

        return str(message_broker.storage._storage)
        # return str(answer)

        # return User.query.all().count()
