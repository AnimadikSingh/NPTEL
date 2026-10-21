import json
import re

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

page_map = {p["page"]: p for p in pages}

print(f"Loaded {len(pages)} pages and {len(lectures)} lectures.")
