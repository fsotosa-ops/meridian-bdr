from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


class MeridianScraper:
    def __init__(self, user_data_dir="./data/browser_session"):
        self.user_data_dir = user_data_dir

    def get_profiles(self, search_url):
        with sync_playwright() as p:
            # Iniciamos el navegador
            context = p.chromium.launch_persistent_context(
                self.user_data_dir,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            page = context.new_page()
            Stealth().apply_stealth_sync(page)
            
            print(f"🕵️ Meridian navegando a: {search_url}")
            
            # Ahora sí, navegamos a la URL que recibimos de main.py
            page.goto(search_url, wait_until="domcontentloaded")
            
            # Esperamos 15 segundos para asegurar carga y login manual si hace falta
            print("Esperando carga completa...")
            page.wait_for_timeout(60000) 

            # Scroll para cargar perfiles dinámicos
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(4000)

            # Extraemos los perfiles
            profile_cards = page.query_selector_all('.artdeco-entity-lockup')
            print(f"📦 Perfiles detectados: {len(profile_cards)}")
            
            results = []
            for card in profile_cards:
                results.append(card.inner_text())
                
            context.close()
            return results