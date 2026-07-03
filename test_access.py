import requests
import time

urls = {
    "INDMoney": "https://www.indmoney.com/",
    "Groww": "https://groww.in/",
    "PowerUp Money": "https://www.google.com/search?q=PowerUp+Money", # Just to check connectivity, but let's try finding the real URL
    "Kuvera": "https://kuvera.in/",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

print("Testing with standard 'requests' library:")
for name, url in urls.items():
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"{name} ({url}): {res.status_code}")
        # Print a snippet to see if it's a Cloudflare challenge
        if "cloudflare" in res.text.lower() or "captcha" in res.text.lower():
            print(f"  -> WARNING: Might be blocked (Cloudflare/Captcha detected)")
    except Exception as e:
        print(f"{name} ({url}): Error - {e}")
    time.sleep(1)
