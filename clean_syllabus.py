import json
import re

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("course_structure.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

def clean_lecture_info(lec):
    p_num = lec["start_page"]
    page_data = pages[p_num - 1]
    raw_lines = page_data["lines"]
    
    # Defaults
    week_num = None
    week_title = ""
    lecture_num = None
    lecture_title = ""
    instructor = ""
    
    txt = "\n".join(raw_lines)
    
    # Instructor
    if "Surojit Mookherjee" in txt:
        instructor = "Prof. Surojit Mookherjee (VGSoM, IIT Kharagpur)"
    elif "Saini Das" in txt:
        instructor = "Prof. Saini Das (VGSoM, IIT Kharagpur)"
    elif "Kunal Kanti Ghosh" in txt:
        instructor = "Prof. Kunal Kanti Ghosh (VGSoM, IIT Kharagpur)"
        
    for line in raw_lines:
        w_m = re.search(r'Week\s*(\d+)[:\s]*(.*)', line, re.I)
        mod_m = re.search(r'Module\s*(\d+)[:\s]*(.*)', line, re.I)
        lec_m = re.search(r'Lecture\s*(\d+)[:\s]*(.*)', line, re.I)
        
        if w_m and not week_num:
            week_num = int(w_m.group(1))
            if w_m.group(2).strip():
                week_title = w_m.group(2).strip()
        elif mod_m and not week_num:
            # In some modules, e.g. Module 02 -> Week 2, Module 08 -> Week 8, Module 09 -> Week 9, Module 11 -> Week 11
            mod_val = int(mod_m.group(1))
            week_num = mod_val
            if mod_m.group(2).strip():
                week_title = mod_m.group(2).strip()
                
        if lec_m and not lecture_num:
            lecture_num = int(lec_m.group(1))
            if lec_m.group(2).strip():
                lecture_title = lec_m.group(2).strip()
                
    # If lecture title is not found in Lecture line, check subsequent lines
    if not lecture_title:
        # Check line after lecture marker
        for i, l in enumerate(raw_lines):
            if "Lecture" in l or "Module" in l:
                if i + 1 < len(raw_lines) and not any(k in raw_lines[i+1] for k in ["NPTEL", "IIT", "VGSoM", "Prof"]):
                    lecture_title = raw_lines[i+1]
                    break
                    
    return {
        "index": lec["index"],
        "start_page": lec["start_page"],
        "end_page": lec["end_page"],
        "page_count": lec["page_count"],
        "week_num": week_num,
        "week_title": week_title,
        "lecture_num": lecture_num,
        "lecture_title": lecture_title,
        "instructor": instructor,
        "raw_lines": raw_lines
    }

curated = [clean_lecture_info(l) for l in lectures]
for c in curated:
    print(f"Lec {c['index']:02d} | Wk {c['week_num']} ({c['week_title']}) | L{c['lecture_num']}: {c['lecture_title']} | P{c['start_page']}-P{c['end_page']}")

with open("curated_lectures.json", "w", encoding="utf-8") as f:
    json.dump(curated, f, ensure_ascii=False, indent=2)
