import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

for p in pages:
    if 322 <= p['page'] <= 328:
        print(f"\n--- PAGE {p['page']} ---")
        for line in p['lines']:
            print(f"  {line}")
