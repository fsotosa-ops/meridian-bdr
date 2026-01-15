#!/usr/bin/env python3
"""
MERIDIAN-BDR v2.7
Agente de prospección automatizado con menú de comandos completo.
"""

import os
import sys
import time
import hashlib
from datetime import datetime
from dotenv import load_dotenv

from src.sheets import SheetsInterface
from src.scraper import MeridianScraper
from src.researcher_api import CompanyResearcherAPI
from src.brain import MeridianBrain
from src.notifier import EmailNotifier

load_dotenv()

def generate_lead_id(name, company):
    raw_string = f"{name.lower().strip()}|{company.lower().strip()}"
    return hashlib.md5(raw_string.encode()).hexdigest()[:12]

def get_config(sheets):
    config = {}
    try:
        icp = sheets.read_range("Config!B2")
        config['icp'] = icp[0][0] if icp and icp[0] else ""
        queries = sheets.read_range("Config!B3")
        config['research_queries'] = queries[0][0] if queries and queries[0] else "{company} importador México"
        url = sheets.read_range("Config!B4")
        config['sales_nav_url'] = url[0][0] if url and url[0] else os.getenv("SALES_NAV_LIST_URL")
        max_pages = sheets.read_range("Config!B5")
        config['max_pages'] = int(max_pages[0][0]) if max_pages and max_pages[0] else 3
        max_leads = sheets.read_range("Config!B6")
        config['max_leads_day'] = int(max_leads[0][0]) if max_leads and max_leads[0] else 50
    except:
        config = {'icp': "", 'research_queries': "", 'sales_nav_url': os.getenv("SALES_NAV_LIST_URL"), 'max_pages': 3, 'max_leads_day': 50}
    return config

def update_last_run(sheets):
    sheets.update_cell("Config!B8", datetime.now().strftime("%Y-%m-%d %H:%M"))

def scrape_and_save():
    print("\n=== PASO 1: EXTRACCIÓN ===")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheets = SheetsInterface(sheet_id)
    config = get_config(sheets)
    
    search_url = config['sales_nav_url']
    if not search_url: return print("❌ Error: Falta URL Sales Nav")
    
    scraper = MeridianScraper()
    brain = MeridianBrain()
    
    existing_data = sheets.read_range("Leads!A2:A") 
    existing_ids = set(row[0] for row in existing_data if row)
    
    print(f"📊 Leads existentes: {len(existing_ids)}")
    
    raw_profiles_data = scraper.get_profiles(search_url, max_pages=config['max_pages'])
    print(f"\n📦 Perfiles encontrados: {len(raw_profiles_data)}")
    
    saved = 0
    for item in raw_profiles_data:
        if saved >= config['max_leads_day']: break
        time.sleep(2)
        
        try:
            analysis = brain.extract_profile_info(item['text'])
            if analysis and analysis.get('name'):
                name = analysis.get('name', '').strip()
                company = analysis.get('company', '')
                lead_id = generate_lead_id(name, company)
                
                if lead_id in existing_ids:
                    print(f"   ⚠️ Duplicado: {name}")
                    continue
                
                print(f"   💾 Nuevo: {name}")
                row = [
                    lead_id, datetime.now().strftime("%Y-%m-%d"), name, analysis.get('role', ''), company,
                    "Sales Navigator", "", "", "", "", item['url'], "🔄 Pendiente", ""
                ]
                sheets.append_row("Leads!A2", row)
                saved += 1
                existing_ids.add(lead_id)
        except: continue
    
    update_last_run(sheets)
    print(f"✅ Guardados: {saved}")
    return saved

def research_and_evaluate():
    print("\n=== PASO 2: INVESTIGACIÓN ===")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheets = SheetsInterface(sheet_id)
    config = get_config(sheets)
    researcher = CompanyResearcherAPI()
    brain = MeridianBrain()
    
    leads = sheets.read_range("Leads!A2:L500")
    if not leads: return [], 0, 0
    
    pending_indices = [i for i, r in enumerate(leads) if len(r) > 11 and "Pendiente" in r[11]]
    print(f"📊 Pendientes: {len(pending_indices)}")
    
    qualified, processed, discarded = [], 0, 0
    
    for i in pending_indices:
        time.sleep(1)
        row = leads[i]
        
        if len(row) < 5: continue
        name, role, company = row[2], row[3], row[4]
        # Recuperar URL original (Columna K, indice 10)
        original_linkedin_url = row[10] if len(row) > 10 else ""
        
        print(f"\n🔍 Analizando: {company}")
        
        import_info, serper_urls = researcher.search_import_data(company, config['research_queries'])
        full_info_text = f"{import_info}\n\nFuentes:\n" + "\n".join(serper_urls[:2])
        full_profile = f"Nombre: {name}\nCargo: {role}\nEmpresa: {company}\nINFO:{import_info}"
        time.sleep(1)
        
        try:
            ev = brain.evaluate_candidate(full_profile, config['icp'])
            if ev:
                score, fit, reason = ev.get('score', 0), ev.get('fit', False), ev.get('reason', '')
                status = "🔍 Revisar" if score >= 70 else ("🤔 Evaluar" if score >= 40 else "❌ Descartado")
                if not fit: discarded += 1
                if score >= 70: 
                    qualified.append({'name': name, 'role': role, 'company': company, 'score': score, 'reason': reason})

                row_num = i + 2
                # Escribimos G..L preservando K (URL original)
                sheets.update_range(f"Leads!G{row_num}:L{row_num}", [[
                    score, 
                    "✅" if fit else "❌", 
                    reason[:200], 
                    full_info_text[:900], 
                    original_linkedin_url, # PROTEGIDA
                    status
                ]])
                print(f"   Score: {score}")
                processed += 1
        except Exception as e: print(f"Error: {e}")

    update_last_run(sheets)
    return qualified, processed, discarded

def send_notification(qualified, total, discarded):
    print("\n=== PASO 3: NOTIFICACIÓN ===")
    notifier = EmailNotifier()
    stats = {'total': total, 'qualified': len(qualified), 'discarded': discarded}
    qualified.sort(key=lambda x: x.get('score', 0), reverse=True)
    notifier.send_daily_summary(stats, qualified)

def run_full():
    scrape_and_save()
    q, t, d = research_and_evaluate()
    if t > 0: send_notification(q, t, d)

# === MENÚ DE COMANDOS RESTAURADO ===
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "full": run_full()
        elif cmd == "scrape": scrape_and_save()
        elif cmd == "research":
            q, t, d = research_and_evaluate()
            if t > 0: send_notification(q, t, d)
        elif cmd == "test-email":
            # Invocamos la prueba del notificador
            from src.notifier import test_email
            test_email()
        elif cmd == "status":
            print("Usa el comando status original si lo necesitas.")
        else:
            print(f"Comando desconocido: {cmd}")
            print("Uso: python main.py [full | scrape | research | test-email]")
    else:
        print("Uso: python main.py [full | scrape | research | test-email]")