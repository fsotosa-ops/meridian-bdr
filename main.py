import os
from dotenv import load_dotenv
from src.sheets import SheetsInterface
from src.scraper import MeridianScraper
from src.brain import MeridianBrain

load_dotenv()

def run_meridian():
    # 1. Obtenemos las variables del .env
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    search_url = os.getenv("SALES_NAV_LIST_URL") # <-- LA URL VIENE DE AQUÍ

    if not search_url:
        print("❌ ERROR: No se encontró SALES_NAV_LIST_URL en el archivo .env")
        return

    # 2. Inicializamos componentes
    sheets = SheetsInterface(sheet_id)
    scraper = MeridianScraper()
    brain = MeridianBrain()

    print("--- Iniciando Meridian-BDR ---")
    
    # 3. Leer ICP de la pestaña Config
    icp_criteria = sheets.read_range("Config!A2")[0][0]
    
    # 4. Lanzar Scraper pasándole la URL
    raw_profiles = scraper.get_profiles(search_url)
    
    print(f"Se encontraron {len(raw_profiles)} candidatos potenciales.")

    # 3. Analizar y filtrar
    for raw_text in raw_profiles:
        analysis = brain.evaluate_candidate(raw_text, icp_criteria)
        
        if analysis and analysis.get('fit'):
            print(f"🎯 Match encontrado: {analysis['summary']['name']}")
            
            # 4. Guardar en Sheets
            row = [
                datetime.now().strftime("%Y-%m-%d"),
                analysis['summary']['name'],
                analysis['summary']['role'],
                analysis['summary']['company'],
                "Ver en Sales Navigator", # Aquí podrías extraer el link real
                analysis['score'],
                analysis['reason']
            ]
            sheets.append_row("Leads!A2", row)
        else:
            print("Skipping...")

if __name__ == "__main__":
    run_meridian()