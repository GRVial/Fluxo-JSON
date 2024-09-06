import os
import json
import boto3
from GoogleAPIClient import GoogleAPIClient
from refactor_form import get_new_form

GOOGLE_API_AUTH_FILE = os.environ.get('GOOGLE_API_AUTH_FILE')

def handler(event, context):
    query_params = event.get('queryStringParameters', {})
    response_type = query_params.get('type', 'json')
    try:
        ssm = boto3.client('ssm')
        google_credentials_str = ssm.get_parameter(Name=GOOGLE_API_AUTH_FILE)['Parameter']['Value']
        google_credentials = json.loads(google_credentials_str)
        google_api_client = GoogleAPIClient(google_credentials)

        if response_type == 'listForms':
            forms = google_api_client.list_google_forms()
            response = {
                'statusCode': 200,
                'body': json.dumps(forms, ensure_ascii=False),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }
            return response
        elif response_type == 'json':
            form_id = query_params.get('formId')
            form_dict = google_api_client.get_form_json(form_id)
            new_form_dict = get_new_form(form_dict)
            response = {
                'statusCode': 200,
                'body': json.dumps(new_form_dict, ensure_ascii=False),
                'headers': {
                    'Content-Type': 'application/json',
                },
            }
            return response
        else:
            response = {
                'statusCode': 400,
                'body': 'Tipo de request inválido',
            }
            return response
    except Exception as e:
        print('Exception:', e)
        response = {
            'statusCode': 500,
            'body': 'Erro ao buscar forms',
        }
        return response
