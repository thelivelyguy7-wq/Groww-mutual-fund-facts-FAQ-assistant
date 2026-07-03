import asyncio
from playwright.async_api import async_playwright

async def test_scrape(url):
    print(f"Testing {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(3000)
            html = await page.content()
            print(f"Length: {len(html)}")
            print("Expense Ratio in HTML:", "Expense Ratio" in html)
            print("Exit Load in HTML:", "Exit Load" in html)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_scrape("https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"))
    asyncio.run(test_scrape("https://www.indmoney.com/mutual-funds/hdfc-small-cap-fund-direct-growth"))
