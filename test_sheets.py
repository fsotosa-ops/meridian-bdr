import os
from dotenv import load_dotenv
from src.sheets import SheetsInterface

# Cargamos las variables del archivo .env
load_dotenv()

# Aquí es donde estaba el error: ahora leemos del .env
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def test():
    print(f"Conectando a la hoja: {SPREADSHEET_ID}...")
    
    # Inicializamos la interfaz
    try:
        sheets = SheetsInterface(SPREADSHEET_ID)
        
        # 1. Intentar leer el ICP (Asegúrate que la pestaña se llame 'Config')
        print("Intentando leer pestaña 'Config'...")
        config = sheets.read_range("Config!A2")
        print(f"✅ Datos leídos: {config}")
        
        # 2. Intentar escribir (Asegúrate que la pestaña se llame 'Leads')
        print("Intentando escribir en pestaña 'Leads'...")
        datos_prueba = ["2026-01-14", "Test Meridian", "Agente", "Lab", "url.com", "10", "Conexión perfecta"]
        sheets.append_row("Leads!A2", datos_prueba)
        
        print("🚀 ¡ÉXITO! Revisa tu Google Sheet, deberías ver los datos.")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")

if __name__ == "__main__":
    test()