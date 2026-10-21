import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

# Inspect pages for a few lectures, e.g. LEC-10 (ERP overview), LEC-20 (Mfg Planning), LEC-30 (IS Strategy)
def inspect_lec(lec_id):
    lec = next(l for l in lectures if l['id'] == lec_id)
    print(f"\n=== Lecture: {lec['id']} - {lec['title']} (P{lec['start_page']}-P{lec['end_page']}) ===")
    for p in pages:
        if lec['start_page'] <= p['page'] <= lec['end_page']:
            lines = [l.strip() for l in p['lines'] if l.strip()]
            if lines and not any(term in lines[0].lower() for term in ["thank you", "reference"]):
                title = lines[0] if lines else "No title"
                bullets = [l for l in lines[1:] if len(l) > 15]
                print(f"  P{p['page']}: {title[:60]} ({len(bullets)} detail lines)")

inspect_lec("LEC-10")
inspect_lec("LEC-20")
inspect_lec("LEC-32")
