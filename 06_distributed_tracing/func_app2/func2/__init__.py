import logging

import azure.functions as func


def main(msg: func.QueueMessage):
    logging.info('func2 queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
