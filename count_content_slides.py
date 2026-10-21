import json

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

print(f"Total lectures: {len(lectures)}")
total_content_slides = 0
for lec in lectures:
    s_page = lec["start_page"]
    e_page = lec["end_page"]
    content_slides = 0
    for p in range(s_page, e_page + 1):
        lines = pages[p - 1]["lines"]
        txt = " ".join(lines).upper()
        if len(lines) > 2 and "THANK YOU" not in txt and "REFERENCES" not in txt and "LEARNING OBJECTIVES" not in txt:
            content_slides += 1
    total_content_slides += content_slides

print(f"Total content slides across all lectures: {total_content_slides} (out of 1163 total pages)")
