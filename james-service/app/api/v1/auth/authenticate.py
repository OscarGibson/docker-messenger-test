import requests
from flask import request
from helpers.functions.responses import ErrorResponse

def authenticate(f):
	def decorated_function(obj, *args, **kwargs):

		headers = {
			'content-type' : 'application/json',
			'Authorization' : request.headers.get('Authorization')
		}
		url = 'http://users-service:5000/api/v1/auth/check-auth'

		response = requests.get(url, headers= headers)

		if response.status_code != 200:
			print(response.status_code)
			return ErrorResponse(
				message= "Invalid token",
				code= response.status_code
				).data

		return f(obj, *args, user_data= response.json()['data'], **kwargs)
	return decorated_function