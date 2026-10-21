import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

page_map = {p["page"]: p for p in pages}

def summarize_week(w_num):
    w_lecs = [l for l in lectures if l["week_num"] == w_num]
    print(f"\n==========================================")
    print(f"WEEK {w_num:02d}: {w_lecs[0]['week_title']} ({len(w_lecs)} Lectures)")
    print(f"==========================================")
    for l in w_lecs:
        print(f"\n-- {l['id']}: {l['title']} (P{l['start_page']}-P{l['end_page']}) --")
        for p_num in range(l["start_page"], l["end_page"] + 1):
            p = page_map.get(p_num)
            if not p:
                continue
            lines = [line.strip() for line in p["lines"] if line.strip()]
            if not lines:
                continue
            # Filter title/thank you
            first = lines[0].lower()
            if any(term in first for term in ["thank you", "reference"]):
                continue
            # Print slide title and key bullets
            title = lines[0][:70]
            bullets = [b[:80] for b in lines[1:5]]
            print(f"  [P{p_num}] {title}")
            for b in bullets:
                print(f"       * {b}")

summarize_week(1)
