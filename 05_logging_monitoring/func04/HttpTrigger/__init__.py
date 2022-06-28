import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Func04 HttpTrigger start...')

    logging.critical('Func04 critical.') # 5
    logging.error('Func04 error.')       # 4
    logging.warning('Func04 warning.')   # 3
    logging.info('Func04 info.')         # 2
    logging.debug('Func04 debug.')       # 1
    #logging.trace('Func04 trace.')       # 0

    return func.HttpResponse(
         "Func04 is working...",
         status_code=200
    )