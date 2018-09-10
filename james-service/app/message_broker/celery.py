from celery import Celery

celery_app = Celery(
	'test_celery', 
	broker= 'amqp://admin:mypass@10.211.55.12:5672', 
	backend= 'rpc://', 
	include= ['test_celery.tasks']
	)