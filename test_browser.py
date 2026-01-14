from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Veremos si abre la ventana
        page = browser.new_page()
        page.goto("https://www.google.com")
        print(f"✅ Título de la página: {page.title()}")
        browser.close()

if __name__ == "__main__":
    test()