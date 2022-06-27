import logging

import azure.functions as func

from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import config_integration

OpenCensusExtension.configure()

logger = logging.getLogger(__name__)

def main(req: func.HttpRequest, context) -> func.HttpResponse:
    logging.info('Container Python HTTP trigger function processed a request.')

    # You must use context.tracer to create spans
    with context.tracer.span("parent"):
        logger.critical('critical Message from Docker Container') # 4
        logger.error('error Message from Docker Container')       # 3
        logger.warning('waring Message from Docker Container')    # 2
        logger.info('info Message from Docker Container')         # 1
        logger.debug('debug Message from Docker Container')       # これは出力されない？

    return func.HttpResponse( "im working (w/ python docker container.)", status_code=200 )



