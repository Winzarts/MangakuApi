from playwright.sync_api import sync_playwright

def get_dynamic_html(url: str) -> str:
    """Mengambil HTML dari halaman dinamis menggunakan Playwright (headless Chromium)."""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            locale="id=ID",
            timezone_id="Asia/Jakarta"
        )

        page = context.new_page()

        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            page.goto(url, timeout=15000, wait_until="domcontentloaded")

            # Tunggu elemen seperti di Selenium
            page.wait_for_selector("div.bge", timeout=15000)

            html = page.content()
        finally:
            context.close()
            browser.close()

        return html
