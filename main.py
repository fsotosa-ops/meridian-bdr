#!/usr/bin/env python3
"""
MERIDIAN-BDR v2.5
Agente de prospección automatizado para BDRs con UUID y Trazabilidad
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
    """Genera un ID único y constante basado en nombre y empresa para evitar duplicados"""
    raw_string = f"{name.lower().strip()}|{company.lower().strip()}"
    return hashlib.md5(raw_string.encode()).hexdigest()[:12]

def get_config(sheets):
    """Lee toda la configuración del Sheet"""
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
        
    except Exception as e:
        print(f"⚠️ Error leyendo config, usando defaults: {e}")
        config = {
            'icp': "",
            'research_queries': "{company} importador México",
            'sales_nav_url': os.getenv("SALES_NAV_LIST_URL"),
            'max_pages': 3,
            'max_leads_day': 50
        }
    return config


def update_last_run(sheets):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheets.update_cell("Config!B8", now)


def scrape_and_save():
    """Paso 1: Extrae de Sales Navigator con UUID Hash, Upsert y Paginación"""
    print("\n" + "="*60)
    print("🕵️  PASO 1: EXTRACCIÓN DE SALES NAVIGATOR")
    print("="*60)
    
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheets = SheetsInterface(sheet_id)
    config = get_config(sheets)
    
    search_url = config['sales_nav_url']
    if not search_url:
        print("❌ ERROR: No se encontró URL de Sales Navigator")
        return 0
    
    scraper = MeridianScraper()
    brain = MeridianBrain()
    
    # 1. LEER IDs EXISTENTES (Columna A)
    existing_data = sheets.read_range("Leads!A2:A") 
    existing_ids = set()
    if existing_data:
        for row in existing_data:
            if row: existing_ids.add(row[0])
            
    print(f"📊 Leads existentes en base de datos: {len(existing_ids)}")
    print(f"📋 Configuración: Max páginas: {config['max_pages']} | Max nuevos/día: {config['max_leads_day']}")
    
    # Extraer perfiles (recibe lista de dicts con url)
    raw_profiles_data = scraper.get_profiles(search_url, max_pages=config['max_pages'])
    print(f"\n📦 Se encontraron {len(raw_profiles_data)} perfiles brutos")
    
    saved_count = 0
    
    for item in raw_profiles_data:
        if saved_count >= config['max_leads_day']:
            print("🛑 Límite diario alcanzado.")
            break
            
        time.sleep(2) 
        
        try:
            raw_text = item['text']
            profile_url = item['url']
            
            analysis = brain.extract_profile_info(raw_text)
            
            if analysis and analysis.get('name'):
                name = analysis.get('name', '').strip()
                company = analysis.get('company', '')
                role = analysis.get('role', '')
                
                # GENERAR ID DETERMINÍSTICO (Hash)
                lead_id = generate_lead_id(name, company)
                
                # CHECK DUPLICADOS POR ID
                if lead_id in existing_ids:
                    print(f"   ⚠️ Duplicado saltado (ID existente): {name}")
                    continue
                
                print(f"   💾 Nuevo [{lead_id}]: {name} - {company}")
                
                row = [
                    lead_id,         # A: ID Hash
                    datetime.now().strftime("%Y-%m-%d"), # B
                    name,            # C
                    role,            # D
                    company,         # E
                    "Sales Navigator", # F: Fuente
                    "",              # G: Score
                    "",              # H: Fit
                    "",              # I: Razón
                    "",              # J: Info
                    profile_url,     # K: URL Perfil (Nueva columna)
                    "🔄 Pendiente",  # L: Status
                    ""               # M: Notas
                ]
                sheets.append_row("Leads!A2", row)
                saved_count += 1
                existing_ids.add(lead_id)
                
        except Exception as e:
            print(f"      ❌ Error procesando perfil: {e}")
            continue
    
    update_last_run(sheets)
    print(f"\n✅ Paso 1 completado: {saved_count} nuevos leads guardados")
    return saved_count


def research_and_evaluate():
    """Paso 2: Investiga empresas y evalúa fit"""
    print("\n" + "="*60)
    print("🔬 PASO 2: INVESTIGACIÓN Y CALIFICACIÓN")
    print("="*60)
    
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheets = SheetsInterface(sheet_id)
    config = get_config(sheets)
    
    researcher = CompanyResearcherAPI()
    brain = MeridianBrain()
    
    # Leemos rango ampliado para incluir ID en col A
    # A=ID, B=Fecha, C=Nombre... L=Status
    leads = sheets.read_range("Leads!A2:M500")
    if not leads:
        print("📭 No hay leads para investigar")
        return [], 0, 0
    
    # Filtramos por status "Pendiente" que está en la columna L (índice 11)
    pending = [i for i, row in enumerate(leads) 
               if len(row) > 11 and "Pendiente" in row[11]]
    
    print(f"📊 Leads pendientes: {len(pending)}")
    
    processed = 0
    qualified_leads = []
    discarded = 0
    
    for i in pending:
        time.sleep(1) # Pausa seguridad
        
        row = leads[i]
        # Índices desplazados por el ID
        lead_id = row[0] if len(row) > 0 else "N/A"
        name = row[2] if len(row) > 2 else ""
        role = row[3] if len(row) > 3 else ""
        company = row[4] if len(row) > 4 else ""
        
        if not company: continue
        
        print(f"\n🔍 [{processed+1}/{len(pending)}] ID:{lead_id[:6]}... {company}")
        
        # Investigar
        import_info, urls = researcher.search_import_data(company, config['research_queries'])
        urls_text = "\n".join(urls[:3]) if urls else ""
        
        # Evaluar
        full_profile = f"Nombre: {name}\nCargo: {role}\nEmpresa: {company}\nINFO:{import_info}"
        
        time.sleep(1) # Pausa Gemini
        
        try:
            evaluation = brain.evaluate_candidate(full_profile, config['icp'])
            
            if evaluation:
                score = evaluation.get('score', 0)
                fit = evaluation.get('fit', False)
                reason = evaluation.get('reason', '')
                
                if score >= 70:
                    status = "🔍 Revisar"
                    qualified_leads.append({
                        'name': name,
                        'role': role,
                        'company': company,
                        'score': score,
                        'reason': reason
                    })
                elif score >= 40:
                    status = "🤔 Evaluar"
                else:
                    status = "❌ Descartado"
                    discarded += 1
                
                # Actualizar fila (Columnas G a L)
                # G=Score, H=Fit, I=Razon, J=Info, K=URLs, L=Status
                row_number = i + 2
                sheets.update_range(f"Leads!G{row_number}:L{row_number}", [[
                    score,
                    "✅" if fit else "❌",
                    reason[:200],
                    import_info[:400],
                    urls_text,
                    status
                ]])
                
                emoji = "✅" if fit else "❌"
                print(f"   {emoji} Score: {score}")
                
        except Exception as e:
            print(f"   ❌ Error evaluando: {e}")
            
        processed += 1
    
    update_last_run(sheets)
    print(f"\n✅ Paso 2 completado: {processed} leads procesados")
    return qualified_leads, processed, discarded


def send_notification(qualified_leads, total, discarded):
    print("\n" + "="*60)
    print("📧 PASO 3: NOTIFICACIÓN")
    print("="*60)
    
    notifier = EmailNotifier()
    stats = {'total': total, 'qualified': len(qualified_leads), 'discarded': discarded}
    qualified_leads.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    notifier.send_daily_summary(stats, qualified_leads)


def show_status():
    """Muestra estado actual del sistema"""
    print("\n" + "="*60)
    print("📊 ESTADO DE MERIDIAN-BDR")
    print("="*60)
    
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheets = SheetsInterface(sheet_id)
    # Rango ajustado por columna ID
    leads = sheets.read_range("Leads!A2:M500")
    
    if not leads:
        print("📭 No hay leads en el sistema")
        return
    
    # Status en columna L (índice 11)
    pending = sum(1 for r in leads if len(r) > 11 and "Pendiente" in r[11])
    qualified = sum(1 for r in leads if len(r) > 11 and "Revisar" in r[11])
    
    print(f"Total leads: {len(leads)} | Pendientes: {pending} | Calificados: {qualified}")


def run_full():
    print("\n🚀 MERIDIAN-BDR - FULL RUN")
    total_scraped = scrape_and_save()
    qualified_leads, total_researched, discarded = research_and_evaluate()
    
    if total_researched > 0:
        send_notification(qualified_leads, total_researched, discarded)
    
    show_status()
    print("\n✅ PIPELINE COMPLETADO")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "scrape": scrape_and_save()
        elif command == "research": 
            q, t, d = research_and_evaluate()
            if t > 0: send_notification(q, t, d)
        elif command == "full": run_full()
        elif command == "status": show_status()
        elif command == "test-email":
            from src.notifier import test_email
            test_email()
        else: print(f"❌ Comando desconocido: {command}")
    else:
        print("Uso: python main.py [scrape|research|full|status|test-email]")