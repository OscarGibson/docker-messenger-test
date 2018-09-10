from enum import Enum
from flask import jsonify

class STATUS(Enum):
    ERROR = 'error'
    SUCCESS = 'success'


class AbstractResponse:
    message = 'message'
    body = {}
    def __init__(self): pass

    @property
    def data(self):
        _response = {**{
                    'status' : self.status.value,
                    'message' : self.message
                }, **self.body}
        return jsonify(_response), self.code

class ErrorResponse(AbstractResponse):
    def __init__(self, message= 'Error message', code= 500):
        self.status = STATUS.ERROR
        self.message = message
        self.code = code

class SuccessResponse(AbstractResponse):
    def __init__(self, message= 'Success message', code= 200, **body):
        self.status = STATUS.SUCCESS
        self.message = message
        self.code = code
        self.body = body