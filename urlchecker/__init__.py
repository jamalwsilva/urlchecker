import logging
from urllib import request
import json

import azure.functions as func
from shared_code import request_urls

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    response_body = ''
    result = request_urls(['google.com', 'yahoo.com.br'], 443, 10)
    for item in result:
        response_body += json.dumps(item) + "\n"

    return func.HttpResponse(response_body)
