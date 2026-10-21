import json

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

print(f"Total lectures in course: {len(lectures)}")
for l in lectures:
    print(f"ID: {l['id']} | Wk {l['week_num']:02d} | Lec {l['lecture_num']} | P{l['start_page']}-P{l['end_page']} | {l['title']}")
