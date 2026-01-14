import os
from datetime import datetime
from dotenv import load_dotenv
from src.sheets import SheetsInterface
from src.scraper import MeridianScraper
from src.researcher import CompanyResearcher
from src.brain import MeridianBrain

load_dotenv()


def get_config(sheets):
    """Lee toda la configuración del Sheet"""
    config = {}
    
    # ICP
    icp = sheets.read_range("Config!B2")
    config['icp'] = icp[0][0] if icp and icp[0] else ""
    
    # Research Queries
    queries = sheets.read_range("Config!B3")
    config['research_queries'] = queries[0][0] if queries and queries[0] else "{company} importador México"
    
    return config


def scrape_and_save():
    """Paso 1: Extrae de Sales Navigator y guarda en Sheets"""
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    search_url = os.getenv("SALES_NAV_LIST_URL")

    if not search_url:
        print("❌ ERROR: No se encontró SALES_NAV_LIST_URL en el archivo .env")
        return

    sheets = SheetsInterface(sheet_id)
    scraper = MeridianScraper()
    brain = MeridianBrain()

    print("--- Paso 1: Extrayendo de Sales Navigator ---")
    
    config = get_config(sheets)
    raw_profiles = scraper.get_profiles(search_url, max_pages=3)
    
    print(f"Se encontraron {len(raw_profiles)} perfiles.")

    for raw_text in raw_profiles:
        analysis = brain.extract_profile_info(raw_text)
        
        if analysis:
            print(f"📝 Guardando: {analysis.get('name', 'Sin nombre')} - {analysis.get('company', '')}")
            
            row = [
                datetime.now().strftime("%Y-%m-%d"),
                analysis.get('name', ''),
                analysis.get('role', ''),
                analysis.get('company', ''),
                "Sales Navigator",
                "",  # Score
                "",  # Fit
                "",  # Razón
                "",  # Info Importaciones
                "No"  # Investigado
            ]
            sheets.append_row("Leads!A2", row)

    print("✅ Paso 1 completado.")


def research_and_evaluate():
    """Paso 2: Investiga empresas y evalúa fit"""
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    
    sheets = SheetsInterface(sheet_id)
    researcher = CompanyResearcher()
    brain = MeridianBrain()
    
    print("--- Paso 2: Investigando empresas ---")
    
    config = get_config(sheets)
    print(f"📋 ICP: {config['icp'][:100]}...")
    print(f"🔍 Queries: {config['research_queries']}")
    
    # Leer todos los leads
    leads = sheets.read_range("Leads!A2:J100")
    
    if not leads:
        print("No hay leads para investigar")
        return
    
    for i, row in enumerate(leads):
        investigado = row[9] if len(row) > 9 else "No"
        
        if investigado == "Sí":
            continue
        
        company = row[3] if len(row) > 3 else ""
        name = row[1] if len(row) > 1 else ""
        role = row[2] if len(row) > 2 else ""
        
        if not company:
            continue
            
        print(f"\n🔍 Investigando: {company}")
        
        # Buscar info usando las queries configuradas
        import_info = researcher.search_import_data(company, config['research_queries'])
        
        # Evaluar con toda la info
        full_profile = f"Nombre: {name}, Cargo: {role}, Empresa: {company}\n{import_info}"
        evaluation = brain.evaluate_candidate(full_profile, config['icp'])
        
        if evaluation:
            row_number = i + 2
            sheets.update_row(f"Leads!F{row_number}:J{row_number}", [
                evaluation.get('score', 0),
                "Sí" if evaluation.get('fit') else "No",
                evaluation.get('reason', ''),
                import_info[:500],
                "Sí"
            ])
            print(f"✅ {company}: Score {evaluation.get('score')} - Fit: {evaluation.get('fit')}")
        
    print("\n✅ Paso 2 completado.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "scrape":
            scrape_and_save()
        elif sys.argv[1] == "research":
            research_and_evaluate()
        elif sys.argv[1] == "full":
            scrape_and_save()
            research_and_evaluate()
    else:
        print("Uso:")
        print("  python main.py scrape   → Extrae de Sales Navigator")
        print("  python main.py research → Investiga y evalúa")
        print("  python main.py full     → Ejecuta todo")