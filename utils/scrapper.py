from playwright.sync_api import sync_playwright
from config import HEADERS, TIMEOUT

def get_dynamic_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        context = browser.new_context(
            user_agent=HEADERS["User-Agent"],
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        try:
            # ✅ tunggu DOM saja (lebih cepat dari networkidle)
            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # ✅ kasih waktu HTMX inject data
            page.wait_for_timeout(3000)

            # ✅ selector lebih fleksibel
            try:
                page.wait_for_selector("div[class*='b']", timeout=30000)
            except:
                print("Selector tidak ketemu, lanjut ambil HTML")

            html = page.content()
            return html

        finally:
            browser.close()
