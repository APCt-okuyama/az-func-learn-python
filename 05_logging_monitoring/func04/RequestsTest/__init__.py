import logging

import requests
from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import config_integration

config_integration.trace_integrations(['requests'])
logger = logging.getLogger('MyHttpTriggerLogger')

OpenCensusExtension.configure()

import azure.functions as func

def main(req: func.HttpRequest, context) -> func.HttpResponse:
    logging.info('my opencensus test start working..')

    with context.tracer.span("parent0"):
        logger.info('Message from HttpTrigger')

    with context.tracer.span("parent"):
        response = requests.get(url='https://www.yahoo.co.jp/')
        logging.info(response.text)
    return response.text
    #return "my opencensus test start working."


