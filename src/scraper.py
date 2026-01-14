from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


class MeridianScraper:
    def __init__(self, user_data_dir="./data/browser_session"):
        self.user_data_dir = user_data_dir

    def get_profiles(self, search_url, max_pages=5):
        all_results = []
        
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                self.user_data_dir,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            page = context.new_page()
            Stealth().apply_stealth_sync(page)
            
            for page_num in range(1, max_pages + 1):
                # Construir URL con paginación
                if "page=" in search_url:
                    current_url = search_url.replace(f"page={page_num-1}", f"page={page_num}")
                else:
                    separator = "&" if "?" in search_url else "?"
                    current_url = f"{search_url}{separator}page={page_num}"
                
                print(f"🕵️ Página {page_num}/{max_pages}: {current_url}")
                
                page.goto(current_url, wait_until="domcontentloaded")
                
                # Esperar carga (más corto después de la primera página)
                wait_time = 15000 if page_num == 1 else 5000
                page.wait_for_timeout(wait_time)

                # Scroll para cargar perfiles dinámicos
                for _ in range(3):
                    page.mouse.wheel(0, 1000)
                    page.wait_for_timeout(1500)

                # Extraer perfiles
                profile_cards = page.query_selector_all('.artdeco-entity-lockup')
                print(f"📦 Perfiles en página {page_num}: {len(profile_cards)}")
                
                if len(profile_cards) == 0:
                    print("⚠️ No hay más perfiles. Terminando paginación.")
                    break
                
                for card in profile_cards:
                    all_results.append(card.inner_text())
                
            context.close()
            
        print(f"\n✅ Total perfiles extraídos: {len(all_results)}")
        return all_results