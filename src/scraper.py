"""
Scraper de Sales Navigator con medidas anti-detección
"""

import random
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


class MeridianScraper:
    
    # Configuración de seguridad anti-ban
    SAFE_CONFIG = {
        "min_wait_page": 8,      # Segundos mínimos entre páginas
        "max_wait_page": 15,     # Segundos máximos entre páginas
        "scroll_steps": 4,       # Número de scrolls por página
        "scroll_wait": (1, 3),   # Rango de espera entre scrolls
        "typing_delay": (50, 150),  # Delay al escribir (ms)
    }
    
    def __init__(self, user_data_dir="./data/browser_session"):
        self.user_data_dir = user_data_dir

    def _human_delay(self, min_sec=1, max_sec=3):
        """Pausa aleatoria para simular comportamiento humano"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        return delay

    def _human_scroll(self, page):
        """Scroll gradual como lo haría un humano"""
        for i in range(self.SAFE_CONFIG["scroll_steps"]):
            scroll_amount = random.randint(300, 700)
            page.mouse.wheel(0, scroll_amount)
            
            min_wait, max_wait = self.SAFE_CONFIG["scroll_wait"]
            self._human_delay(min_wait, max_wait)

    def get_profiles(self, search_url, max_pages=3):
        """
        Extrae perfiles de Sales Navigator de forma segura.
        
        Args:
            search_url: URL de búsqueda de Sales Navigator
            max_pages: Número máximo de páginas a scrapear (default: 3)
        
        Returns:
            Lista de textos de perfiles extraídos
        """
        all_results = []
        
        with sync_playwright() as p:
            # Iniciar navegador persistente (mantiene sesión)
            context = p.chromium.launch_persistent_context(
                self.user_data_dir,
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-web-security",
                    "--disable-features=IsolateOrigins,site-per-process"
                ],
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = context.new_page()
            
            # Aplicar stealth
            Stealth().apply_stealth_sync(page)
            
            try:
                for page_num in range(1, max_pages + 1):
                    # Construir URL con paginación
                    if "page=" in search_url:
                        current_url = search_url.replace(
                            f"page={page_num-1}", 
                            f"page={page_num}"
                        )
                    else:
                        separator = "&" if "?" in search_url else "?"
                        current_url = f"{search_url}{separator}page={page_num}"
                    
                    print(f"\n🕵️ Página {page_num}/{max_pages}")
                    
                    # Navegar
                    page.goto(current_url, wait_until="domcontentloaded")
                    
                    # Espera inicial (más larga en primera página para login manual)
                    if page_num == 1:
                        print("   ⏳ Esperando carga inicial (20s para login si es necesario)...")
                        page.wait_for_timeout(20000)
                    else:
                        wait_time = random.randint(
                            self.SAFE_CONFIG["min_wait_page"] * 1000,
                            self.SAFE_CONFIG["max_wait_page"] * 1000
                        )
                        print(f"   ⏳ Esperando {wait_time/1000:.1f}s...")
                        page.wait_for_timeout(wait_time)
                    
                    # Scroll humano para cargar contenido dinámico
                    print("   📜 Scrolling...")
                    self._human_scroll(page)
                    
                    # Extraer perfiles
                    profile_cards = page.query_selector_all('.artdeco-entity-lockup')
                    
                    if len(profile_cards) == 0:
                        # Intentar selector alternativo
                        profile_cards = page.query_selector_all('[data-x--lead-card]')
                    
                    if len(profile_cards) == 0:
                        print("   ⚠️ No se encontraron perfiles. Posible fin de resultados.")
                        break
                    
                    print(f"   📦 Perfiles encontrados: {len(profile_cards)}")
                    
                    for card in profile_cards:
                        try:
                            text = card.inner_text()
                            if text and len(text) > 20:
                                all_results.append(text)
                        except:
                            continue
                    
                    # Pausa entre páginas
                    if page_num < max_pages:
                        delay = self._human_delay(
                            self.SAFE_CONFIG["min_wait_page"],
                            self.SAFE_CONFIG["max_wait_page"]
                        )
                        print(f"   😴 Pausa de {delay:.1f}s antes de siguiente página...")
                        
            except Exception as e:
                print(f"❌ Error durante scraping: {e}")
                
            finally:
                context.close()
        
        print(f"\n✅ Total perfiles extraídos: {len(all_results)}")
        return all_results
