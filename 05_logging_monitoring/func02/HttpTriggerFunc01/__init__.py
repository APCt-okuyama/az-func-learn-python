import logging
import os

import azure.functions as func

import requests

#import shared_code.MyOpenCensus
#logger = logging.getLogger(__name__)

def main(req: func.HttpRequest, context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # You must use context.tracer to create spans
    # with context.tracer.span("parent"):
    #     response = requests.get(url=os.environ["FUNC02_URL_STRING"])
    response = requests.get(url=os.environ["FUNC01_URL_STRING"])

    return func.HttpResponse(
         "Func02 called Func01 ....?",
             status_code=200
    )
