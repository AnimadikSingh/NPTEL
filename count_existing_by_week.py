import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

import gen_weeks_1_3, gen_weeks_4_6, gen_weeks_7_9, gen_weeks_10_12
import gen_extra_w1_w3, gen_extra_w4_w6, gen_extra_w7_w9, gen_extra_w10_w12
import gen_syllabus_deep_bank
import gen_boost_coverage

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

week_existing = {}
seen = set()
for q in sources:
    t = " ".join(q["question"].lower().split())
    if t not in seen:
        seen.add(t)
        w = q["week"]
        week_existing.setdefault(w, []).append(q)

print("Existing Unique Questions Per Week:")
for w in range(1, 13):
    print(f"Week {w:02d}: {len(week_existing.get(w, []))} questions")

total_existing = sum(len(qs) for qs in week_existing.values())
print(f"Total existing questions: {total_existing}")
