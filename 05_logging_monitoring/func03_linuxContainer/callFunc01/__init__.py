import logging
import os
import requests

import azure.functions as func

from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import config_integration

OpenCensusExtension.configure()
config_integration.trace_integrations(['requests'])

logger = logging.getLogger(__name__)

def main(req: func.HttpRequest, context) -> func.HttpResponse:
    logging.info('Container Python HTTP trigger function processed a request.')

    # You must use context.tracer to create spans
    with context.tracer.span("parent"):
        #response = requests.get(url='https://www.yahoo.co.jp/')
        my_url = os.environ["FUNC01_URL_STRING"]
        logger.info('my_url: ' + my_url)
        response = requests.get(url=my_url)  

    return func.HttpResponse( "im working (w/ python docker container. func01)", status_code=200 )



