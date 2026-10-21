import pypdf
import json
import re
import os

pdf_path = "MIS Week 1_merged.pdf"
reader = pypdf.PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"Total pages: {total_pages}")

pages_data = []

for idx, page in enumerate(reader.pages):
    page_num = idx + 1
    raw_text = page.extract_text() or ""
    # Clean up non-ascii or non-printable bullet symbols if needed
    cleaned_lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    pages_data.append({
        "page": page_num,
        "raw_text": raw_text,
        "lines": cleaned_lines,
        "char_count": len(raw_text)
    })

# Save extracted raw pages
with open("extracted_pages.json", "w", encoding="utf-8") as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print("Saved extracted_pages.json")

# Now let's analyze lectures and weeks
markers = []
for p in pages_data:
    txt = "\n".join(p["lines"])
    # Match title slides like "Week 01:", "Module 02:", "Lecture 01", etc.
    # Often title slides have "Management Information System" and "Prof."
    is_title_slide = False
    week_match = re.search(r'(Week\s*\d+|Module\s*\d+)', txt, re.I)
    lec_match = re.search(r'(Lecture\s*\d+)', txt, re.I)
    
    if "Management Information System" in txt and (week_match or lec_match):
        is_title_slide = True
    elif p["lines"] and ("Week " in p["lines"][0] or "Module " in p["lines"][0] or "Lecture " in p["lines"][0]):
        is_title_slide = True
        
    if is_title_slide or week_match or lec_match:
        markers.append({
            "page": p["page"],
            "lines": p["lines"][:5]
        })

print(f"Detected {len(markers)} potential structure markers.")
with open("markers.json", "w", encoding="utf-8") as f:
    json.dump(markers, f, ensure_ascii=False, indent=2)
print("Saved markers.json")
