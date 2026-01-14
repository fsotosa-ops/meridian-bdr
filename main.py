#!/usr/bin/env python3
"""
MERIDIAN-BDR v2.0
Agente de prospección automatizado para BDRs

Uso:
    python main.py scrape     # Extrae de Sales Navigator
    python main.py research   # Investiga y califica
    python main.py full       # Ejecuta todo
    python main.py status     # Muestra estado actual
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

from src.sheets import SheetsInterface
from src.scraper import MeridianScraper
from src.researcher_api import CompanyResearcherAPI
from src.brain import MeridianBrain
from src.notifier import EmailNotifier

load_dotenv()


def get_config(sheets):
    """Lee toda la configuración del Sheet"""
    config = {}
    
    try:
        # Leer configuración (B2:B7)
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
        
        auto_run = sheets.read_range("Config!B7")
        config['auto_run'] = auto_run[0][0].lower() == "sí" if auto_run and auto_run[0] else False
        
    except Exception as e:
        print(f"⚠️ Error leyendo config, usando defaults: {e}")
        config = {
            'icp': "",
            'research_queries': "{company} importador México",
            'sales_nav_url': os.getenv("SALES_NAV_LIST_URL"),
            'max_pages': 3,
            'max_leads_day': 50,
            'auto_run': False
        }
    
    return config


def update_last_run(sheets):
    """Actualiza timestamp de última ejecución"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheets.update_cell("Config!B8", now)


def scrape_and_save():
    """Paso 1: Extrae de Sales Navigator y guarda en Sheets"""
    print("\n" + "="*60)
    print("🕵️  PASO 1: EXTRACCIÓN DE SALES NAVIGATOR")
    print("="*60)
    
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheets = SheetsInterface(sheet_id)
    config = get_config(sheets)
    
    search_url = config['sales_nav_url']
    if not search_url:
        print("❌ ERROR: No se encontró URL de Sales Navigator")
        print("   Configúrala en Config!B4 o en el archivo .env")
        return 0
    
    scraper = MeridianScraper()
    brain = MeridianBrain()
    
    print(f"📋 Configuración:")
    print(f"   • Max páginas: {config['max_pages']}")
    print(f"   • Max leads/día: {config['max_leads_day']}")
    print(f"   • URL: {search_url[:50]}...")
    
    # Extraer perfiles
    raw_profiles = scraper.get_profiles(search_url, max_pages=config['max_pages'])
    print(f"\n📦 Se encontraron {len(raw_profiles)} perfiles")
    
    # Limitar por día
    profiles_to_process = raw_profiles[:config['max_leads_day']]
    saved_count = 0
    
    for raw_text in profiles_to_process:
        analysis = brain.extract_profile_info(raw_text)
        
        if analysis and analysis.get('name'):
            print(f"   💾 {analysis.get('name', 'N/A')} - {analysis.get('company', 'N/A')}")
            
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
                "",  # Fuentes/URLs
                "🔄 Pendiente",  # Status
                ""   # Notas BDR
            ]
            sheets.append_row("Leads!A2", row)
            saved_count += 1
    
    update_last_run(sheets)
    print(f"\n✅ Paso 1 completado: {saved_count} leads guardados")
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
    
    print(f"📋 ICP: {config['icp'][:80]}...")
    print(f"🔍 Queries: {config['research_queries'][:60]}...")
    
    # Leer leads pendientes
    leads = sheets.read_range("Leads!A2:L500")
    
    if not leads:
        print("📭 No hay leads para investigar")
        return [], 0, 0
    
    pending = [i for i, row in enumerate(leads) 
               if len(row) > 10 and "Pendiente" in row[10]]
    
    print(f"📊 Leads pendientes: {len(pending)}")
    
    processed = 0
    qualified_leads = []
    discarded = 0
    
    for i in pending:
        row = leads[i]
        
        company = row[3] if len(row) > 3 else ""
        name = row[1] if len(row) > 1 else ""
        role = row[2] if len(row) > 2 else ""
        
        if not company:
            continue
        
        print(f"\n🔍 [{processed+1}/{len(pending)}] {company}")
        
        # Investigar (ahora retorna tuple con URLs)
        import_info, urls = researcher.search_import_data(company, config['research_queries'])
        
        # Formatear URLs para el Sheet (máximo 3)
        urls_text = "\n".join(urls[:3]) if urls else ""
        
        # Evaluar
        full_profile = f"""
        Nombre: {name}
        Cargo: {role}
        Empresa: {company}
        
        INFORMACIÓN DE IMPORTACIONES:
        {import_info}
        """
        
        evaluation = brain.evaluate_candidate(full_profile, config['icp'])
        
        if evaluation:
            score = evaluation.get('score', 0)
            fit = evaluation.get('fit', False)
            reason = evaluation.get('reason', '')
            
            # Determinar status basado en score
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
            
            # Actualizar fila (ahora incluye columna de URLs)
            row_number = i + 2
            sheets.update_range(f"Leads!F{row_number}:K{row_number}", [[
                score,
                "✅" if fit else "❌",
                reason[:200],
                import_info[:400],
                urls_text,
                status
            ]])
            
            emoji = "✅" if fit else "❌"
            print(f"   {emoji} Score: {score} - {reason[:50]}...")
        
        processed += 1
    
    update_last_run(sheets)
    print(f"\n✅ Paso 2 completado: {processed} leads procesados")
    
    return qualified_leads, processed, discarded


def send_notification(qualified_leads, total, discarded):
    """Envía notificación por email al BDR"""
    print("\n" + "="*60)
    print("📧 PASO 3: NOTIFICACIÓN")
    print("="*60)
    
    notifier = EmailNotifier()
    
    stats = {
        'total': total,
        'qualified': len(qualified_leads),
        'discarded': discarded
    }
    
    # Ordenar por score
    qualified_leads.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    success = notifier.send_daily_summary(stats, qualified_leads)
    
    if success:
        print("✅ Notificación enviada")
    else:
        print("⚠️ Notificación no enviada (email no configurado)")


def show_status():
    """Muestra estado actual del sistema"""
    print("\n" + "="*60)
    print("📊 ESTADO DE MERIDIAN-BDR")
    print("="*60)
    
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheets = SheetsInterface(sheet_id)
    
    # Leer leads
    leads = sheets.read_range("Leads!A2:L500")
    
    if not leads:
        print("📭 No hay leads en el sistema")
        return
    
    # Contar por status
    total = len(leads)
    pending = sum(1 for r in leads if len(r) > 10 and "Pendiente" in r[10])
    to_review = sum(1 for r in leads if len(r) > 10 and "Revisar" in r[10])
    to_evaluate = sum(1 for r in leads if len(r) > 10 and "Evaluar" in r[10])
    discarded = sum(1 for r in leads if len(r) > 10 and "Descartado" in r[10])
    to_crm = sum(1 for r in leads if len(r) > 10 and "CRM" in r[10])
    
    print(f"""
    📈 RESUMEN:
    ─────────────────────────────
    Total leads:        {total}
    🔄 Pendientes:      {pending}
    🔍 Para revisar:    {to_review}
    🤔 Para evaluar:    {to_evaluate}
    ❌ Descartados:     {discarded}
    ✅ Enviados a CRM:  {to_crm}
    ─────────────────────────────
    """)
    
    # Top leads
    high_score = [(r[1], r[3], r[5]) for r in leads 
                  if len(r) > 5 and r[5] and str(r[5]).isdigit() and int(r[5]) >= 70]
    
    if high_score:
        print("    🏆 TOP LEADS (Score ≥70):")
        for name, company, score in high_score[:5]:
            print(f"       • {name} @ {company}: {score}")


def run_full():
    """Ejecuta pipeline completo"""
    print("\n" + "="*60)
    print("🚀 MERIDIAN-BDR - EJECUCIÓN COMPLETA")
    print("="*60)
    
    # Paso 1: Scrape
    total_scraped = scrape_and_save()
    
    # Paso 2: Research
    qualified_leads, total_researched, discarded = research_and_evaluate()
    
    # Paso 3: Notificar
    if total_researched > 0:
        send_notification(qualified_leads, total_researched, discarded)
    
    # Mostrar status
    show_status()
    
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETADO")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "scrape":
            scrape_and_save()
        elif command == "research":
            qualified_leads, total, discarded = research_and_evaluate()
            if total > 0:
                send_notification(qualified_leads, total, discarded)
        elif command == "full":
            run_full()
        elif command == "status":
            show_status()
        elif command == "test-email":
            from src.notifier import test_email
            test_email()
        else:
            print(f"❌ Comando desconocido: {command}")
            print(__doc__)
    else:
        print(__doc__)
        print("\nEjemplo: python main.py full")
