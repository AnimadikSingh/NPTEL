import json
import re

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("curated_lectures.json", "r", encoding="utf-8") as f:
    curated = json.load(f)

# Let's inspect the actual title slide for each of the 60 lectures
for c in curated:
    p = pages[c["start_page"] - 1]
    lines = [l.strip() for l in p["lines"] if l.strip()]
    print(f"Index {c['index']:02d} | Page {c['start_page']}: {lines}")
