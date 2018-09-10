import requests
from app.message_broker import producer, receiver
from helpers.functions.random import generate_random_string
import time

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


def send_message(consumer_name, consumer_type, body, *args, **kwargs):

	start_time = time.time()

	uuid = generate_random_string(16)

	try:
		producer.send_message(
			consumer_name= consumer_name, 
			consumer_type= consumer_type,
			uuid= uuid,
			body= body
			)
	except Exception as e:
		return {
			'status' : 'error',
			'message' : str(e)
		}

	while True:
		if receiver.have_message(uuid):
			return {
				'status' : 'success',
				'message' : '',
				'data' : receiver.get_message(uuid)
			}
		if time.time() - start_time > 5:
			return {
				'status' : 'error',
				'message' : 'timeout'
			}
	
