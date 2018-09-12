from . import producer, receiver, storage, manager, services
from threading import Thread
from time import time

class MessageBroker:
    def __init__(self, rabbit_mq_path, current_queue_name, timeout= 5):
        self.timeout = timeout
        self.rabbit_mq_path = rabbit_mq_path
        self.current_queue_name = current_queue_name
        self.storage = storage.Storage()
        self.producer = producer.Producer(self.rabbit_mq_path, self.current_queue_name)
        self.manager = manager.Manager()
        self.receiver = receiver.Receiver(
            self.rabbit_mq_path,
            self.current_queue_name,
            self.storage,
            self.producer,
            self.manager
            )


    def init_app(self, app):
        setattr(app, 'message_broker', self)
        t = Thread(target= self.receiver.run)
        t.setDaemon(True)
        t.start()

    def send_and_wait(self, receiver_name, question):
        start_time = time()

        uuid = services.generate_random_string(16)

        self.producer.send_message(
        				uuid= uuid,
        				receiver_name= receiver_name,
        				question= question,
        				forward= True
        				)

        while True:
            if self.storage.have_message(uuid):
                response = self.storage.get_message(uuid)
                self.storage.remove_message(uuid)
                return response
            if time() - start_time > self.timeout:
                return "Timeout error"
