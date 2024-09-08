import os
import json
import boto3
from GoogleAPIClient import GoogleAPIClient
from RequestHandler import RequestHandler

GOOGLE_API_AUTH_FILE = os.environ.get('GOOGLE_API_AUTH_FILE')

def handler(event, context):
    ssm = boto3.client('ssm')
    google_credentials_str = ssm.get_parameter(Name=GOOGLE_API_AUTH_FILE)['Parameter']['Value']
    google_credentials = json.loads(google_credentials_str)
    GoogleAPIClient.set_API_credentials(google_credentials)

    return RequestHandler.handle(event)
