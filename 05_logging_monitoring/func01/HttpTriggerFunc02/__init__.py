import logging
import os

import azure.functions as func

import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    response = requests.get(url=os.environ["FUNC02_URL_STRING"])

    return func.HttpResponse(
         "Func01 called Func02 ....?",
             status_code=200
    )
