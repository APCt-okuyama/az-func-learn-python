import logging
import os
import azure.functions as func
import redis

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    r = redis.StrictRedis(host=os.environ["MyAzureRedisHOST"],
        port=6380, db=0, password=os.environ["MyAzureRedisKey"], ssl=True)
    r.set('foo', 'bar12345')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
