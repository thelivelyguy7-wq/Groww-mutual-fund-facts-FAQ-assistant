import os
import json
from bs4 import BeautifulSoup
import re

INPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")

def clean_html():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    manifest_path = os.path.join(INPUT_DIR, "manifest.json")
    if not os.path.exists(manifest_path):
        print("Manifest not found. Run scraper.py first.")
        return
        
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    for item in manifest:
        if item.get("status") not in ["success", "skipped"]:
            continue
            
        filename = item["filename"]
        if not filename.endswith(".html"):
            continue
            
        file_path = os.path.join(INPUT_DIR, filename)
        
        print(f"Cleaning {filename}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
                
            soup = BeautifulSoup(html, "html.parser")
            
            # Remove scripts, styles, headers, footers
            for elements in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                elements.decompose()
                
            # Try to format tables nicely
            for table in soup.find_all("table"):
                table_text = "\n"
                for row in table.find_all("tr"):
                    cells = row.find_all(["th", "td"])
                    row_text = " | ".join([cell.get_text(strip=True) for cell in cells])
                    table_text += row_text + "\n"
                table.replace_with(table_text)
                
            text = soup.get_text(separator="\n", strip=True)
            
            # Remove multiple newlines
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            output_data = {
                "url": item["url"],
                "fund_name": item["title"] or filename.replace("-", " ").replace(".html", "").title(),
                "content": text
            }
            
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".html", ".json"))
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=4)
                
        except Exception as e:
            print(f"Failed to clean {filename}: {e}")
            
    print("Done cleaning HTML.")

if __name__ == "__main__":
    clean_html()
