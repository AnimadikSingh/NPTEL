import json

with open('final_lectures.json', 'r', encoding='utf-8') as f:
    lectures = json.load(f)

with open('extracted_pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

page_map = {p['page']: p for p in pages}

print(f"Total mapped lectures: {len(lectures)}")
week_pages = {}
for l in lectures:
    w = l['week_num']
    week_pages.setdefault(w, []).extend(range(l['start_page'], l['end_page'] + 1))

for w in range(1, 13):
    pgs = week_pages.get(w, [])
    # Filter out title / thank you / reference pages
    content_pgs = []
    for p_num in pgs:
        p = page_map.get(p_num)
        if not p:
            continue
        lines = [l.strip() for l in p['lines'] if l.strip()]
        if not lines:
            continue
        first_line = lines[0].lower()
        if any(term in first_line for term in ["thank you", "reference"]):
            continue
        if len(lines) <= 2 and any(t in first_line for t in ["management information systems", "lecture"]):
            continue
        content_pgs.append(p_num)
    print(f"Week {w:02d}: {len(pgs)} total slides, {len(content_pgs)} content-bearing slides")
