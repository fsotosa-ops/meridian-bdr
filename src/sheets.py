"""
Interface con Google Sheets para Meridian-BDR
"""

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class SheetsInterface:
    
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.creds = self._authenticate()
        self.service = build('sheets', 'v4', credentials=self.creds)

    def _authenticate(self):
        """Autentica con Google Sheets API"""
        creds = None
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def read_range(self, range_name):
        """
        Lee datos de un rango.
        
        Args:
            range_name: Rango en formato 'Sheet!A1:B10'
        
        Returns:
            Lista de filas (cada fila es una lista de celdas)
        """
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            return result.get('values', [])
        except HttpError as err:
            print(f"❌ Error leyendo {range_name}: {err}")
            return None

    def append_row(self, range_name, values):
        """
        Añade una fila al final del rango.
        
        Args:
            range_name: Rango donde añadir (ej: 'Leads!A2')
            values: Lista con valores de la fila
        """
        try:
            body = {'values': [values]}
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()
        except HttpError as err:
            print(f"❌ Error añadiendo fila: {err}")

    def update_range(self, range_name, values):
        """
        Actualiza un rango de celdas.
        
        Args:
            range_name: Rango a actualizar (ej: 'Leads!F2:J2')
            values: Lista de filas con valores
        """
        try:
            body = {'values': values}
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
        except HttpError as err:
            print(f"❌ Error actualizando {range_name}: {err}")

    def update_cell(self, cell, value):
        """
        Actualiza una celda individual.
        
        Args:
            cell: Celda en formato 'Sheet!A1'
            value: Valor a escribir
        """
        self.update_range(cell, [[value]])

    def clear_range(self, range_name):
        """
        Limpia un rango de celdas.
        
        Args:
            range_name: Rango a limpiar
        """
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
        except HttpError as err:
            print(f"❌ Error limpiando {range_name}: {err}")

    def get_sheet_names(self):
        """Obtiene nombres de todas las pestañas"""
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheets = sheet_metadata.get('sheets', [])
            return [s.get('properties', {}).get('title', '') for s in sheets]
        except HttpError as err:
            print(f"❌ Error obteniendo pestañas: {err}")
            return []
