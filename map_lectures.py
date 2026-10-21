import json

with open("markers.json", "r", encoding="utf-8") as f:
    markers = json.load(f)

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

# Let's inspect the exact lines of each marker to extract week, lecture/module, title, and instructor
lectures = []
for i, m in enumerate(markers):
    p_num = m["page"]
    next_p = markers[i+1]["page"] - 1 if i + 1 < len(markers) else len(pages)
    lines = m["lines"]
    lectures.append({
        "index": i + 1,
        "start_page": p_num,
        "end_page": next_p,
        "page_count": next_p - p_num + 1,
        "header_lines": lines
    })

print(f"Total lectures mapped: {len(lectures)}")
for lec in lectures:
    print(f"#{lec['index']:02d}: P{lec['start_page']:04d}-P{lec['end_page']:04d} ({lec['page_count']}p): {' | '.join(lec['header_lines'][:3])}")

with open("course_structure.json", "w", encoding="utf-8") as f:
    json.dump(lectures, f, ensure_ascii=False, indent=2)
