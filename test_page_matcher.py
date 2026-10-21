import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

# Helper to find lecture for a given page
def find_lecture(page_num):
    for lec in lectures:
        if lec["start_page"] <= page_num <= lec["end_page"]:
            return lec
    return None

print(f"Total pages: {len(pages)}, Total lectures: {len(lectures)}")
