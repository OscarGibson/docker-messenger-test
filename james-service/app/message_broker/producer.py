import rabbitpy
import logging
import datetime
import uuid
from helpers.functions.random import generate_random_string


logging.basicConfig(level= logging.DEBUG)

def send_message(consumer_name, data= {}):

    uuid = generate_random_string(16)

    with rabbitpy.Connection('amqp://admin:mypass@rabbitmq:5672/%2f') as conn:

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
                'data' : data,
                'answers' : ['Baby don\'t hurt me!'],
                'forward' : False,
                'from' : 'james',
                'to' : 'nina'
            }

            # Create the msg by passing channel, message and properties (as a dict)
            message = rabbitpy.Message(channel, body)

            # Publish the message
            message.publish(exchange, consumer_name)
            logging.info('AFTER message publish: %s' % consumer_name)

    return uuid
