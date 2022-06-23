import logging

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.critical('This is logging.critical.') # 4
    logging.error('This is logging.error.')       # 3
    logging.warning('This is logging.warning.')   # 2  
    logging.info('This is logging.info.')         # 1
    logging.debug('This is logging.debug.')       # これは出力されない？

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
