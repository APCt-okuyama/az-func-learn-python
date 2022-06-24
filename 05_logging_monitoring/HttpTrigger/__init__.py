import logging

import azure.functions as func

from opencensus.extension.azure.functions import OpenCensusExtension
logger = logging.getLogger('HttpTriggerLogger')

# 初期化
OpenCensusExtension.configure() 

def main(req: func.HttpRequest, context) -> func.HttpResponse:

    logging.critical('This is logging.critical.') # 4
    logging.error('This is logging.error.')       # 3
    logging.warning('This is logging.warning.')   # 2  
    logging.info('This is logging.info.')         # 1
    logging.debug('This is logging.debug.')       # これは出力されない？

    # You must use context.tracer to create spans
    with context.tracer.span("parent"):
        logger.critical('critical Message from HttpTrigger') # 4
        logger.error('error Message from HttpTrigger')       # 3
        logger.warning('waring Message from HttpTrigger')    # 2
        logger.info('info Message from HttpTrigger')         # 1
        logger.debug('debug Message from HttpTrigger')       # これは出力されない？

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. im working (w/ python)")
    else:
        return func.HttpResponse( "im working (w/ python)", status_code=200 )
