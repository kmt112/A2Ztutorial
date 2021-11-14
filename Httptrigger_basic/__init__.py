import azure.functions as func
from flask import render_template, request
import base64, json, logging, os, requests
from requests.structures import CaseInsensitiveDict
import urllib.request, json
import pprint

admin_url = os.environ["ADMIN_URL"]
secret_token = os.environ["SECRET_TOKEN"]
# admin_url = "https://api.json-generator.com/templates/aiT2bGkqZ2Xn/data"
# secret_token = "xx"

def extract_json (content):
  book = []
  for result in content['book']:
    if result['language'] == "Chinese":
      book.append(result['title'])
  return book


def main (req: func.HttpRequest) -> func.HttpResponse:
  try:
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer " + secret_token
    resp = requests.get(admin_url, headers=headers).json()
    logging.info('print json: %s', resp)
    book = extract_json(resp)
    logging.info('chinese books: %s', book)
    json_format = json.dumps(book)
    return func.HttpResponse(json_format, status_code = 200)
  
  except Exception as e:
    logging.exception("Connection Error to API server")
    return func.HttpResponse('Error')