from playwright.sync_api import sync_playwright
from config import HEADERS, TIMEOUT

def get_dynamic_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=HEADERS['User-Agent'],
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        try:
            page.goto(url, timeout=TIMEOUT * 1000)
            page.wait_for_selector("div.bge", timeout=15000)
            html = page.content()
            return html
        finally:
            browser.close()