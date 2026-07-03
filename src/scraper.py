import os
import json
import asyncio
import hashlib
from playwright.async_api import async_playwright

URLS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "urls.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
MAX_RETRIES = 3

def get_urls():
    if not os.path.exists(URLS_FILE):
        print(f"Error: {URLS_FILE} not found.")
        return []
    with open(URLS_FILE, 'r') as f:
        return json.load(f)

async def scrape_url(page, url, hashes):
    fund_slug = url.split("/")[-1]
    
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Scraping: {url} (Attempt {attempt}/{MAX_RETRIES})")
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(3000) # Give dynamic tables time to render
            
            html_content = await page.content()
            title = await page.title()
            
            current_hash = hashlib.sha256(html_content.encode('utf-8')).hexdigest()
            
            if hashes.get(url) == current_hash:
                print(f"No changes detected for {fund_slug}, skipping.")
                return {"url": url, "slug": fund_slug, "filename": f"{fund_slug}.html", "title": title, "status": "skipped", "hash": current_hash}
            
            file_path = os.path.join(OUTPUT_DIR, f"{fund_slug}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Successfully saved {fund_slug}.html")
            return {"url": url, "slug": fund_slug, "filename": f"{fund_slug}.html", "title": title, "status": "success", "hash": current_hash}
            
        except Exception as e:
            print(f"Error on attempt {attempt} for {url}: {e}")
            if attempt < MAX_RETRIES:
                print("Retrying in 5 seconds...")
                await asyncio.sleep(5)
            else:
                print(f"Failed to scrape {url} after {MAX_RETRIES} attempts.")
                return {"url": url, "status": "error", "error": str(e)}

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    urls = get_urls()
    
    hashes_path = os.path.join(OUTPUT_DIR, "hashes.json")
    hashes = {}
    if os.path.exists(hashes_path):
        try:
            with open(hashes_path, 'r', encoding='utf-8') as f:
                hashes = json.load(f)
        except json.JSONDecodeError:
            pass
            
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        for url in urls:
            res = await scrape_url(page, url, hashes)
            results.append(res)
            if res.get("hash"):
                hashes[url] = res["hash"]
            await asyncio.sleep(3)
            
        await browser.close()
        
    with open(hashes_path, 'w', encoding='utf-8') as f:
        json.dump(hashes, f, indent=4)
        
    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    success_count = sum(1 for r in results if r["status"] in ["success", "skipped"])
    print(f"\n--- SCRAPING SUMMARY ---")
    print(f"Total Attempted: {len(urls)}")
    print(f"Total Successful/Skipped: {success_count}")
    
    if success_count != len(urls):
        print(f"WARNING: Expected exactly {len(urls)} files, but got {success_count}.")
    else:
        print(f"SUCCESS: Exactly {len(urls)} HTML files processed.")

if __name__ == "__main__":
    asyncio.run(main())
