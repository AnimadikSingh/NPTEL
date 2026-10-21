import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

import gen_weeks_1_3, gen_weeks_4_6, gen_weeks_7_9, gen_weeks_10_12
import gen_extra_w1_w3, gen_extra_w4_w6, gen_extra_w7_w9, gen_extra_w10_w12
import gen_syllabus_deep_bank
import gen_boost_coverage

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
sources.extend(gen_boost_coverage.get_boost_questions())

seen = set()
unique = []
for q in sources:
    t = " ".join(q["question"].lower().split())
    if t not in seen:
        seen.add(t)
        unique.append(q)

lec_counts = {l["id"]: 0 for l in lectures}
for q in unique:
    lid = q.get("lecture_id")
    if lid in lec_counts:
        lec_counts[lid] += 1

counts = list(lec_counts.values())
print(f"Total lectures: {len(lectures)}")
print(f"Min questions in any lecture: {min(counts)}")
print(f"Max questions in any lecture: {max(counts)}")
print(f"Average questions per lecture: {sum(counts)/len(counts):.1f}")

# Check any with < 5
low = [lid for lid, c in lec_counts.items() if c < 5]
print(f"Lectures with < 5 questions: {len(low)} ({low})")
