import logging
import redis
import os #os.environ["myAppSetting"]
import uuid
from opencensus.extension.azure.functions import OpenCensusExtension


import azure.functions as func
logger = logging.getLogger("func1Trigger")
OpenCensusExtension.configure()

def main(req: func.HttpRequest, context, msg: func.Out[str]) -> func.HttpResponse:
    with context.tracer.span("parent"):
        logging.info('func1Trigger start.')

        myHostname = os.environ["REDIS_HOST"]
        myPassword = os.environ["REDIS_KEY"]
        r = redis.StrictRedis(host=myHostname, port=6380,
                              password=myPassword, ssl=True)

        myid = str(uuid.uuid4())
        result = r.set(myid, "Hello!, The cache is working with Python!")
        result = r.get(myid)

        msg.set(myid)

    return func.HttpResponse("create redis record.")

