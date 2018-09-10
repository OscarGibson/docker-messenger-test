import rabbitpy
import logging
import datetime
import uuid
from time import time


logging.basicConfig(level= logging.DEBUG)

"""
'amqp://admin:mypass@rabbitmq:5672/%2f'
james
"""

class Producer:

    def __init__(self, rabbit_mq_path, current_queue_name):
        self.rabbit_mq_path = rabbit_mq_path
        self.current_queue_name = current_queue_name

    def send_message(self, uuid, consumer_name, question, forward= False, answer= None):

        with rabbitpy.Connection(self.rabbit_mq_path) as conn:

            # Use the channel as a context manager
            with conn.channel() as channel:

                # Create the exchange
                exchange = rabbitpy.Exchange(channel, '%s_exchange' % consumer_name)
                exchange.declare()

                # Create the queue
                queue = rabbitpy.Queue(channel, consumer_name)
                queue.declare()

                # Bind the queue
                queue.bind(exchange, consumer_name)


                body = {
                    'uuid' : uuid,
                    'question' : question,
                    'answer' : answer,
                    'forward' : forward,
                    'from' : self.current_queue_name,
                    'to' : consumer_name,
                    'timestamp' : time(),
                }

                # Create the msg by passing channel, message and properties (as a dict)
                message = rabbitpy.Message(channel, body)

                # Publish the message
                message.publish(exchange, consumer_name)
                logging.info('AFTER message publish: %s' % consumer_name)

        return uuid