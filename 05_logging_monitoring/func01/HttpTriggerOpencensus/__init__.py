import logging
import os
import azure.functions as func

import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler

import shared_code.MyOpenCensus

logger = logging.getLogger(__name__)

# 初期化
def callback_function(envelope):
   envelope.tags['ai.cloud.role'] = 'my_new_role_name'
   return True

handler = AzureLogHandler()
handler.add_telemetry_processor(callback_function)
logger.addHandler(handler)

def main(req: func.HttpRequest, context) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')
    logger.info('__name__ : ' + __name__)

    # You must use context.tracer to create spans
    with context.tracer.span("parent"):
        #response = requests.get(url='https://www.yahoo.co.jp/')
        my_url = os.environ["FUNC02_URL_STRING"]
        logger.info('my_url: ' + my_url)
        response = requests.get(url=my_url)  

    return func.HttpResponse(
         "OpenCensusExtension is working?",
             status_code=200
    )
