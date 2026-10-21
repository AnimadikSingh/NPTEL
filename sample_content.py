import json

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("curated_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

for lec in lectures[:5]:
    print(f"\n=== Lecture {lec['index']}: {lec['lecture_title']} (Pages {lec['start_page']}-{lec['end_page']}) ===")
    slide_texts = []
    for p in range(lec['start_page'], lec['end_page'] + 1):
        txt = " ".join(pages[p-1]["lines"])
        if len(txt) > 30 and not "THANK YOU" in txt.upper() and not "REFERENCES" in txt.upper():
            slide_texts.append(f"P{p}: {txt[:100]}...")
    print("\n".join(slide_texts[:6]))
