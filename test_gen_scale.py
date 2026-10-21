import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

page_map = {p["page"]: p for p in pages}

print(f"Total pages: {len(pages)}, Total lectures: {len(lectures)}")
