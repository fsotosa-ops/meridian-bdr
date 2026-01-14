from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


class CompanyResearcher:
    def __init__(self, user_data_dir="./data/browser_session"):
        self.user_data_dir = user_data_dir
    
    def search_import_data(self, company_name, query_templates):
        """
        Busca información de una empresa en Google.
        
        query_templates: string con queries separadas por coma
        Usa {company} como placeholder para el nombre de la empresa
        Ejemplo: "{company} importador México, {company} volumen importaciones"
        """
        
        # Parsear las queries del template
        queries = [
            q.strip().replace("{company}", company_name) 
            for q in query_templates.split(",")
        ]
        
        all_results = []
        
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                self.user_data_dir,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            page = context.new_page()
            Stealth().apply_stealth_sync(page)
            
            try:
                for query in queries:
                    print(f"  🔎 {query}")
                    
                    page.goto(f"https://www.google.com/search?q={query}", wait_until="domcontentloaded")
                    page.wait_for_timeout(3000)
                    
                    # Extraer snippets
                    results = page.query_selector_all('.g')
                    
                    for result in results[:3]:
                        try:
                            title_el = result.query_selector('h3')
                            snippet_el = result.query_selector('.VwiC3b')
                            
                            if title_el and snippet_el:
                                all_results.append(f"{title_el.inner_text()}: {snippet_el.inner_text()}")
                        except:
                            continue
                    
                    page.wait_for_timeout(2000)
                    
            finally:
                context.close()
        
        return " | ".join(all_results) if all_results else "Sin información encontrada"