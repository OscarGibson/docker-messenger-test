from app.message_broker.manager import Manager

import logging
logging.basicConfig(level= logging.INFO)

logging.info("IMPORT JAMES MANAGER")

class JamesManager(Manager):

	def mult_numbers(self, x, y):
		return x * y
