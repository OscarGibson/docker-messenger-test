#!/usr/bin/env python
import logging
import rabbitpy
from .producer import send_message

URL = 'amqp://admin:mypass@rabbitmq:5672/%2f?heartbeat=15'

logging.basicConfig(level= logging.INFO)

def run_consumer():
    print("--- RUNNING CONSUMER ---")
    i = 0
    while True:
        with rabbitpy.Connection(URL) as conn:
            logging.info('OPEN CONNECTION')
            with conn.channel() as channel:
                logging.info('OPEN CHANEL')
                # Exit on CTRL-C
                i += 1
                try:
                    for message in rabbitpy.Queue(channel, 'james'):
                        if i % 1000 == 0:
                            logging.info('------------  PING  ------------ %i' % i)
                        logging.info("GET MESSAGE")
                        logging.info(dir(message))
                        logging.info(message.body)
                        logging.info("GET MESSAGE END")
                        message.pprint(True)
                        message.ack()
                except KeyboardInterrupt:
                    logging.info('Exited consumer "user"')

    logging.info('--- END OF CONSUMER LOOP ---')
