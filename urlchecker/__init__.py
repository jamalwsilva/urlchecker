import logging
import requests
import json
import socket

import azure.functions as func
from shared_code import request_urls, DEFAULT_PORT, DEFAULT_DAYS_THRESHOLD

URLS_LOCATION = 'https://devcelurlchecker9d86.blob.core.windows.net/devcelurlchecker-files/urls.txt?sp=r&st=2022-05-18T14:12:39Z&se=2023-02-01T22:12:39Z&sv=2020-08-04&sr=b&sig=XvX6yevYP2YCjHwM%2BtwGHoJlbspcBtmSRvebJTuumms%3D'

def download_urls():
    result = requests.get(URLS_LOCATION)
    if result.status_code == 200:
        return [line.strip() for line in result.text.split('\n')]
    logging.error(f'Could not fetch {URLS_LOCATION}')
    return []


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    socket.setdefaulttimeout(2)

    response_body = ''
    result = request_urls(download_urls(), DEFAULT_PORT, DEFAULT_DAYS_THRESHOLD)
    for item in result:
        response_body += json.dumps(item) + "\n"

    return func.HttpResponse(response_body)
