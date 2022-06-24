import logging

import azure.functions as func

import requests

import shared_code.MyOpenCensus
logger = logging.getLogger(__name__)

# 初期化

def main(req: func.HttpRequest, context) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')

    # You must use context.tracer to create spans
    with context.tracer.span("parent"):
        response = requests.get(url='https://www.yahoo.co.jp/')

    return func.HttpResponse(
         "OpenCensusExtension is working?",
             status_code=200
    )
