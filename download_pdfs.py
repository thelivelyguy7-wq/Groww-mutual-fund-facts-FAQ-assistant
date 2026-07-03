import requests

urls = {
    "hdfc_small_cap_sid.pdf": "https://www.hdfcfund.com/api/v1/download-document/4060",
    "hdfc_large_cap_sid.pdf": "https://www.hdfcfund.com/api/v1/download-document/4054",
    "hdfc_balanced_adv_sid.pdf": "https://www.hdfcfund.com/api/v1/download-document/4050"
}

import os
os.makedirs("data/raw", exist_ok=True)

for name, url in urls.items():
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
    if res.status_code == 200 and res.content.startswith(b"%PDF"):
        with open(f"data/raw/{name}", "wb") as f:
            f.write(res.content)
        print(f"Downloaded {name}")
    else:
        print(f"Failed to download {name}: {res.status_code}, not a PDF")
