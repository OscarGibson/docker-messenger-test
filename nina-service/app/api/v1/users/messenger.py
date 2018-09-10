import requests

class Messenger:

	def __init__(self, receiver, *args, **kwargs):
		self.receiver = receiver
		self.headers = {
			'content-type' : 'application/json',
		}

	def set_headers(self, request_object):
		self.headers['Authorization'] = request_object.headers.get('Authorization')

	def send(self, data= {}, method= 'get', params= ''):
		# print("SENFING: ", self.receiver % params)
		return getattr(requests, method)(self.receiver % params, json= data, headers= self.headers)