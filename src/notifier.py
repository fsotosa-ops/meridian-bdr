"""
Notificaciones seguras usando Gmail API (OAuth 2.0)
Integrado con templates Sumadots y diseño SaaS.
"""

import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from src.templates import get_daily_summary_html

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.send'
]

class EmailNotifier:
    
    def __init__(self):
        self.bdr_email = os.getenv("BDR_EMAIL")
        self.sheet_url = os.getenv("GOOGLE_SHEET_URL", "")
        self.creds = self._authenticate()
        
        if self.creds:
            self.service = build('gmail', 'v1', credentials=self.creds)
        else:
            self.service = None
            print("⚠️ No se pudo autenticar Gmail API")

    def _authenticate(self):
        """Autenticación unificada OAuth 2.0"""
        creds = None
        
        if os.path.exists('token.json'):
            try:
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except Exception:
                creds = None
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try: creds.refresh(Request())
                except: creds = None
            
            if not creds:
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print("❌ Error: No se encontró credentials.json")
                    return None
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def send_daily_summary(self, stats, top_leads):
        """Envía el email usando la API de Gmail y el template Premium"""
        
        if not self.service or not self.bdr_email:
            print("📧 Notificación saltada (Faltan credenciales o BDR_EMAIL)")
            return False
        
        # Logo de LinkedIn Sumadots
        logo_url = "https://media.licdn.com/dms/image/v2/C4E0BAQGkX9289qHnZA/company-logo_200_200/company-logo_200_200/0/1630646698687?e=2147483647&v=beta&t=H-W6i3GvU5x-r7qC9d_L2XvXyZ7_qYy_z2_x4_w5_v6"
        
        # Generar HTML desde el módulo limpio
        html_content = get_daily_summary_html(stats, top_leads, self.sheet_url, logo_url)

        try:
            message = EmailMessage()
            message.set_content("Tu cliente de correo no soporta HTML.")
            message.add_alternative(html_content, subtype='html')
            
            message['To'] = self.bdr_email
            message['Subject'] = f"🟣 Meridian: {stats.get('qualified', 0)} Oportunidades detectadas"

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'raw': encoded_message}

            self.service.users().messages().send(userId="me", body=create_message).execute()
            print(f"✅ Notificación Sumadots enviada a {self.bdr_email}")
            return True

        except HttpError as error:
            print(f"❌ Error enviando notificación: {error}")
            return False

# --- FUNCIÓN DE PRUEBA (FUERA DE LA CLASE) ---
def test_email():
    """Prueba de envío con datos falsos"""
    print("🚀 Iniciando prueba de email...")
    
    # Aquí instanciamos la clase, que ya está definida arriba
    notifier = EmailNotifier()
    
    # Datos simulados para probar el diseño
    stats = {"total": 45, "qualified": 3, "discarded": 12}
    leads = [
        {
            "name": "Roberto Díaz", 
            "role": "CTO", 
            "company": "TechLatam", 
            "score": 92, 
            "reason": "Stack tecnológico 100% compatible. Presupuesto Q1 aprobado para migración cloud."
        },
        {
            "name": "Ana Vega", 
            "role": "VP Engineering", 
            "company": "SoftCorp", 
            "score": 78, 
            "reason": "Empresa en expansión. Ana es decisora técnica aunque el ciclo de venta puede ser largo."
        },
        {
            "name": "Carlos Ruiz", 
            "role": "DevOps Lead", 
            "company": "StartUp X", 
            "score": 45, 
            "reason": "Empresa muy pequeña, probablemente sin presupuesto Enterprise."
        }
    ]
    
    result = notifier.send_daily_summary(stats, leads)
    if result:
        print("✅ Email de prueba enviado correctamente.")
    else:
        print("❌ Falló el envío del email.")

if __name__ == "__main__":
    test_email()