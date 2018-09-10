from app.message_broker.manager import Manager


class JamesManager(Manager):
	
	@staticmethod
	def mult_numbers(x, y):
		return x * y