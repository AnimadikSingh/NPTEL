import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

import gen_weeks_1_3, gen_weeks_4_6, gen_weeks_7_9, gen_weeks_10_12
import gen_extra_w1_w3, gen_extra_w4_w6, gen_extra_w7_w9, gen_extra_w10_w12
import gen_syllabus_deep_bank

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

sources = []
for w in range(1, 13):
    sources.extend(importlib.import_module(f'bank_generators.week{w:02d}').get_questions())

sources.extend(gen_weeks_1_3.get_questions_w1_w3())
sources.extend(gen_weeks_4_6.get_questions_w4_w6())
sources.extend(gen_weeks_7_9.get_questions_w7_w9())
sources.extend(gen_weeks_10_12.get_questions_w10_w12())

sources.extend(gen_extra_w1_w3.get_extra_questions())
sources.extend(gen_extra_w4_w6.get_extra_questions())
sources.extend(gen_extra_w7_w9.get_extra_questions())
sources.extend(gen_extra_w10_w12.get_extra_questions())

sources.extend(gen_syllabus_deep_bank.get_deep_questions())

seen = set()
unique = []
for q in sources:
    t = " ".join(q["question"].lower().split())
    if t not in seen:
        seen.add(t)
        unique.append(q)

lec_map = {l["id"]: l for l in lectures}
lec_counts = {l["id"]: 0 for l in lectures}

for q in unique:
    lid = q.get("lecture_id")
    if lid in lec_counts:
        lec_counts[lid] += 1

print("Lectures with fewer than 6 questions:")
for lid, cnt in lec_counts.items():
    if cnt < 6:
        l = lec_map[lid]
        print(f"  {lid} (Wk {l['week_num']:02d} Lec {l['lecture_num']}): {cnt} qs - {l['title']} (P{l['start_page']}-P{l['end_page']})")
