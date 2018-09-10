from app.message_broker.manager import Manager


class NinaManager(Manager):
	
	@staticmethod
	def add_numbers(x, y):
		return x + y