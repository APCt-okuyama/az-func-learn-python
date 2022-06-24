import logging

import azure.functions as func

import requests
from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import config_integration

config_integration.trace_integrations(['requests'])
logger = logging.getLogger('HttpTriggerLogger')
# 初期化
OpenCensusExtension.configure() 

def main(req: func.HttpRequest, context) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')

    # You must use context.tracer to create spans
    with context.tracer.span("parent"):
        response = requests.get(url='https://www.yahoo.co.jp/')

    return func.HttpResponse(
         "OpenCensusExtension is working?",
             status_code=200
    )
