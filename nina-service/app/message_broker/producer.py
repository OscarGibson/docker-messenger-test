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

    def send_message(self, uuid, receiver_name, question, forward= False, answer= None):

        with rabbitpy.Connection(self.rabbit_mq_path) as conn:

            # Use the channel as a context manager
            with conn.channel() as channel:

                # Create the exchange
                exchange = rabbitpy.Exchange(channel, '%s_exchange' % receiver_name)
                # exchange = rabbitpy.Exchange(channel, '%s_exchange' % "james")
                exchange.declare()

                # Create the queue
                queue = rabbitpy.Queue(channel, receiver_name)
                # queue = rabbitpy.Queue(channel, "james")
                queue.declare()

                # Bind the queue
                queue.bind(exchange, receiver_name)
                # queue.bind(exchange, "james")


                body = {
                    'uuid' : uuid,
                    'question' : question,
                    'forward' : forward,
                    'from' : self.current_queue_name,
                    'to' : receiver_name,
                    'timestamp' : time(),
                }

                # body = {
                #     'uuid' : uuid,
                #     'question' : question,
                #     'forward' : True,
                #     'from' : "nina",
                #     'to' : "james",
                #     'timestamp' : time(),
                # }


                # Create the msg by passing channel, message and properties (as a dict)
                message = rabbitpy.Message(channel, body)

                # Publish the message
                message.publish(exchange, receiver_name)
                # message.publish(exchange, "james")
                logging.info('AFTER message publish: %s' % receiver_name)

        return uuid