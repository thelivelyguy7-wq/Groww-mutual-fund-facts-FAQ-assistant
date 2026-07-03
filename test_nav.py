import asyncio
import re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        await page.goto('https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth', wait_until="load", timeout=60000)
        await page.wait_for_timeout(5000)
        await page.screenshot(path="screenshot.png", full_page=True)
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator='\n\n', strip=True)
        
        matches = re.findall(r'.{0,50}158.{0,50}', text, re.IGNORECASE)
        for m in matches[:5]:
            print(m.encode('ascii', 'ignore').decode())
        
        print("Finding 'NAV' in text:")
        nav_matches = re.findall(r'.{0,50}NAV.{0,50}', text, re.IGNORECASE)
        for m in nav_matches[:5]:
            print(m.encode('ascii', 'ignore').decode())
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
