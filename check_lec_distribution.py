import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

import gen_weeks_1_3
import gen_weeks_4_6
import gen_weeks_7_9
import gen_weeks_10_12

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

bg = []
for w in range(1, 13):
    mod = importlib.import_module(f'bank_generators.week{w:02d}')
    bg.extend(mod.get_questions())

gw = []
gw.extend(gen_weeks_1_3.get_questions_w1_w3())
gw.extend(gen_weeks_4_6.get_questions_w4_w6())
gw.extend(gen_weeks_7_9.get_questions_w7_w9())
gw.extend(gen_weeks_10_12.get_questions_w10_w12())

# Combine without duplicate questions
all_q = []
seen = set()
for q in bg:
    t = q['question'].strip().lower()
    if t not in seen:
        seen.add(t)
        all_q.append(q)

for q in gw:
    t = q['question'].strip().lower()
    if t not in seen:
        seen.add(t)
        all_q.append(q)

print(f"Total combined unique questions so far: {len(all_q)}")

lec_counts = {}
for q in all_q:
    lid = q.get('lecture_id')
    lec_counts[lid] = lec_counts.get(lid, 0) + 1

print("\nLecture Question Distribution:")
for l in lectures:
    lid = l['id']
    cnt = lec_counts.get(lid, 0)
    print(f"{lid} (Wk {l['week_num']:02d} Lec {l['lecture_num']}): {cnt} questions ({l['title']})")
