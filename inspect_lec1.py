import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

for p_num in range(1, 18):
    p = pages[p_num - 1]
    cleaned = [l.strip() for l in p["lines"] if l.strip()]
    print(f"--- Page {p_num} ---")
    for l in cleaned:
        # replace non-ascii bullet
        l_clean = l.encode('ascii', errors='replace').decode('ascii')
        print("  ", l_clean)
