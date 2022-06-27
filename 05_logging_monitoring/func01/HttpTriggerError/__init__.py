import logging
import os

import azure.functions as func
from opencensus.ext.azure.log_exporter import AzureLogHandler

import shared_code.MyOpenCensus
logger = logging.getLogger(__name__)

def callback_function(envelope):
   envelope.tags['ai.cloud.role'] = 'my_new_role_name2'
   return True
#handler = AzureLogHandler(connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"])
handler = AzureLogHandler()
handler.add_telemetry_processor(callback_function)
logger.addHandler(handler)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logger.info('This is Python throw exception!')
    raise ValueError("my exception!")
    return func.HttpResponse("This is Python throw exception!")

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
