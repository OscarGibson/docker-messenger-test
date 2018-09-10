#!/usr/bin/env python
import logging
import rabbitpy
# from .producer import send_message

"""
URL = 'amqp://admin:mypass@rabbitmq:5672/%2f?heartbeat=15'
james
"""

logging.basicConfig(level= logging.INFO)

class Receiver:

    def __init__(self, rabbit_mq_path, current_queue_name, storage, producer, manager):
        self.rabbit_mq_path = rabbit_mq_path
        self.current_queue_name = current_queue_name
        self.storage = storage
        self.producer = producer
        self.manager = manager

    def run(self):
        print("--- RUNNING RECEIVER ---")
        i = 0
        while True:
            with rabbitpy.Connection(self.rabbit_mq_path) as conn:
                logging.info('OPEN CONNECTION')
                with conn.channel() as channel:
                    logging.info('OPEN CHANEL')
                    # Exit on CTRL-C
                    try:
                        for message in rabbitpy.Queue(channel, self.current_queue_name):

                            message_json = message.json()
                            logging.info("GET MESSAGE")
                            logging.info("MESSAGE : %s" % str(message_json))

                            if message_json['forward']:
                                logging.info("SEND FORWARD TO %s" % message_json['from'])
                                answer = self.manager.run_function(message_json['question'])
                                data = {
                                    'answer' : answer,
                                    'question' : message_json['question']
                                }
                                self.producer.send_message(
                                    uuid= message_json['uuid'], 
                                    consumer_name= message_json['from'], 
                                    forward= False,
                                    question= message_json['question'], 
                                    answer= answer)
                            else:
                                logging.info("SAVE TO STORAGE - <%s>" % message_json['uuid'])
                                logging.info("MESSAGE: %s" % str(message_json))
                                self.storage.add_message(message_json['uuid'], message_json['answer'])

                            logging.info("GET MESSAGE END")
                            # message.pprint(True)
                            # message.ack()
                    except KeyboardInterrupt:
                        logging.info('Exited consumer "user"')

        logging.info('--- END OF RECEIVER LOOP ---')