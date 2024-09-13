import json
from GoogleAPIClient import GoogleAPIClient
from RefactorForm import RefactorForm


class RequestHandler:

    @staticmethod
    def handle(event:dict) -> dict:
        handler = RequestHandler.get_handler(event)

        if handler is None:
            return RequestHandler._response_404('Not found')

        method = event['requestContext']['http']['method']
        if (method not in handler['allowed_methods']):
            return {
                'statusCode': 405,
                'body': 'Method not allowed',
            }
        
        try:
            handler_method = handler['handler']
            return handler_method(event, method)

        except Exception as e:
            print('Exception:', e)
            return {
            'statusCode': 500,
            'body': 'Internal server error',
        }

    @staticmethod
    def get_handler(event):
        path = event.get('rawPath')

        handler = RequestHandler.endpoints.get(path, None)

        if handler is None and path[-1] == '/':
            handler = RequestHandler.endpoints.get(path[:-1], None)

        return handler

    @staticmethod
    def list_forms_handler(event:dict, method:str) -> dict:
        google_api_client = GoogleAPIClient()
        forms = google_api_client.list_google_forms()
        response = {
            'statusCode': 200,
            'body': json.dumps(forms, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
        return response

    @staticmethod
    def get_form_handler(event:dict, method:str) -> dict:
        google_api_client = GoogleAPIClient()

        query_params = event.get('queryStringParameters', {})
        form_id = query_params.get('formId', None)

        if form_id is None:
            return {
            'statusCode': 400,
            'body': 'Missing form id'
        }

        form_dict = google_api_client.get_form_json(form_id)

        if form_dict is None:
            return RequestHandler._response_404('Form id not found')

        new_form_dict = RefactorForm.get_new_form(form_dict)
        response = {
            'statusCode': 200,
            'body': json.dumps(new_form_dict, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
        return response
    
    @staticmethod
    def _response_404(message):
        return {
            'statusCode': 404,
            'body': message
        }

    endpoints = {
        '/listForms' : {
        'allowed_methods': ('GET',),
        'handler': list_forms_handler
        },
        '/': {
        'route': '/',
        'allowed_methods': ('GET',),
        'handler': get_form_handler
        }
    }
