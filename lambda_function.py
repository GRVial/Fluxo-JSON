import sys
import os
import json
import boto3
from GoogleAPIClient import GoogleAPIClient

GOOGLE_API_AUTH_FILE = os.environ['GOOGLE_API_AUTH_FILE']

def handler(event, context):
    try:
        ssm = boto3.client('ssm')
        google_credentials_str = ssm.get_parameter(GOOGLE_API_AUTH_FILE)['Parameter']['Value']
        google_credentials = json.loads(google_credentials_str)

        google_api_client = GoogleAPIClient(google_credentials)
        forms = google_api_client.list_google_forms()

        forms_jsons = [google_api_client.get_form_json(f['id']) for f in forms]

        response = {
            'statusCode': 200,
            'body': json.dumps(forms_jsons, ensure_ascii=False, indent=2),
            'headers': {
                    'Content-Type': 'application/json',
                }
        }
        return response
    except Exception as e:
        print('Exception:', e)
        response = {
            'statusCode': 500,
            'body': 'Erro ao buscar forms',
        }
        return response
