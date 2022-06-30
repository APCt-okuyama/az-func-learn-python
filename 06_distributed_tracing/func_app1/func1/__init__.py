import logging
import os
import uuid
import redis

import azure.functions as func


def main(req: func.HttpRequest, context, msg: func.Out[str]) -> func.HttpResponse:
    logging.info('func1 start...')

    myHostname = os.environ["REDIS_HOST"]
    myPassword = os.environ["REDIS_KEY"]
    r = redis.StrictRedis(host=myHostname, port=6380,
                          password=myPassword, ssl=True)

    myid = str(uuid.uuid4())
    result = r.set(myid, "Hello!, The cache is working with Python!")
    result = r.get(myid)

    msg.set(myid)

    return myid
