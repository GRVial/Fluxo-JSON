import os
import json
import boto3
from GoogleAPIClient import GoogleAPIClient
from refactor_form import get_new_form

GOOGLE_API_AUTH_FILE = os.environ.get('GOOGLE_API_AUTH_FILE')

def handler(event, context):
    try:
        ssm = boto3.client('ssm')
        google_credentials_str = ssm.get_parameter(Name=GOOGLE_API_AUTH_FILE)['Parameter']['Value']
        google_credentials = json.loads(google_credentials_str)
        google_api_client = GoogleAPIClient(google_credentials)
        forms = google_api_client.list_google_forms()

        new_forms_dicts = []
        for form in forms:
            form_dict = google_api_client.get_form_json(form['id'])
            new_form_dict = get_new_form(form_dict)
            new_forms_dicts.append(new_form_dict)

        response = {
            'statusCode': 200,
            'body': json.dumps(new_forms_dicts, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
        return response
    except Exception as e:
        print('Exception:', e)
        response = {
            'statusCode': 500,
            'body': 'Erro ao buscar forms',
        }
        return response
