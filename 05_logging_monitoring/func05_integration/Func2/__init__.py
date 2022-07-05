import logging

from opencensus.extension.azure.functions import OpenCensusExtension

import azure.functions as func
logger = logging.getLogger("func2Trigger")
OpenCensusExtension.configure()

def main(context, msg: func.QueueMessage) -> None:
    with context.tracer.span("parent"):
        logging.info('func2 a queue item: %s',
                 msg.get_body().decode('utf-8'))
