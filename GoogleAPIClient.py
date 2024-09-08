import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json


class GoogleAPIClient:
    _credentials_dict = None

    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/forms.body.readonly']
        self.credentials = self._get_credentials()
        self.drive_service = self._build_drive_service()
        self.forms_service = self._build_forms_service()

    @staticmethod
    def set_API_credentials(credentials_dict: dict):
        GoogleAPIClient._credentials_dict = credentials_dict

    def _get_credentials(self):    
        # Autenticação usando as credenciais da conta de serviço
        credentials = service_account.Credentials.from_service_account_info(
            GoogleAPIClient._credentials_dict, scopes=self.scopes
        )
        return credentials

    def _build_drive_service(self):
        try:
            return build('drive', 'v3', credentials=self.credentials)
        except HttpError as error:
            print(f"Erro ao construir o serviço do Google Drive: {error}")
            raise

    def _build_forms_service(self):
        try:
            return build('forms', 'v1', credentials=self.credentials)
        except HttpError as error:
            print(f"Erro ao construir o serviço do Google Forms: {error}")
            raise

    def list_google_forms(self) -> list[tuple[str, str]]:
        try:
            results = self.drive_service.files().list(
                q="mimeType='application/vnd.google-apps.form'",
                fields="files(id, name)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            print(f"Erro ao listar arquivos do Google Drive: {error}")
            raise

    def get_form_json(self, form_id: str) -> dict:
        try:
            form = self.forms_service.forms().get(formId=form_id).execute()
            return form
        except HttpError as error:
            if error.status_code == 404:
                return None
            
            print(f"Erro ao buscar detalhes do formulário com ID {form_id}: {error}")
            raise
