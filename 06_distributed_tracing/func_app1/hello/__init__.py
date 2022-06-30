import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python hello...')

    return func.HttpResponse("Python hello...")
