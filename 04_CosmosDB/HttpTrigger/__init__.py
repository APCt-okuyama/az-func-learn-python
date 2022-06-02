import logging

import azure.functions as func


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    request_body = req.get_body()

    doc.set(func.Document.from_json(request_body))

    return func.HttpResponse(
        "Cosmos DB binding test is working.",
        status_code=200
    )
