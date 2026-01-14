import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Si modificas estos ámbitos, elimina el archivo token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetsInterface:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.creds = self._authenticate()
        self.service = build('sheets', 'v4', credentials=self.creds)

    def _authenticate(self):
        creds = None
        # El archivo token.json almacena los tokens de acceso del usuario.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Si no hay credenciales válidas, deja que el usuario inicie sesión.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Guarda las credenciales para la próxima ejecución
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def read_range(self, range_name):
        """Lee datos de una pestaña (ej: 'Config!A2:B10')"""
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            return result.get('values', [])
        except HttpError as err:
            print(f"Error leyendo Sheets: {err}")
            return None

    def append_row(self, range_name, values):
        """Añade una fila con los datos del perfil filtrado"""
        try:
            body = {'values': [values]}
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
        except HttpError as err:
            print(f"Error escribiendo en Sheets: {err}")

    def update_row(self, range_name, values):
        """Actualiza celdas específicas"""
        try:
            body = {'values': [values]}
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
        except HttpError as err:
            print(f"Error actualizando Sheets: {err}")
