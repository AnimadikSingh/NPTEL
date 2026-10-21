import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

from validator import validate_question
import gen_weeks_1_3, gen_weeks_4_6, gen_weeks_7_9, gen_weeks_10_12
import gen_extra_w1_w3, gen_extra_w4_w6, gen_extra_w7_w9, gen_extra_w10_w12

bg = []
for w in range(1, 13):
    mod = importlib.import_module(f'bank_generators.week{w:02d}')
    bg.extend(mod.get_questions())

gw = []
gw.extend(gen_weeks_1_3.get_questions_w1_w3())
gw.extend(gen_weeks_4_6.get_questions_w4_w6())
gw.extend(gen_weeks_7_9.get_questions_w7_w9())
gw.extend(gen_weeks_10_12.get_questions_w10_w12())

gx = []
gx.extend(gen_extra_w1_w3.get_extra_questions())
gx.extend(gen_extra_w4_w6.get_extra_questions())
gx.extend(gen_extra_w7_w9.get_extra_questions())
gx.extend(gen_extra_w10_w12.get_extra_questions())

print(f"BG: {len(bg)}, GW: {len(gw)}, GX: {len(gx)}")

combined = []
seen = set()

for q in bg + gw + gx:
    t = q['question'].strip().lower()
    if t not in seen:
        seen.add(t)
        combined.append(q)

print(f"Total Unique Questions: {len(combined)}")

# Check validation
valid = 0
invalid = 0
errors = []

for idx, q in enumerate(combined, 1):
    w = q.get('week', 1)
    lid = q.get('lecture_id', 'LEC-01')
    q['id'] = f"MIS-W{w:02d}-{lid}-{idx:04d}"
    is_valid, msg = validate_question(q)
    if is_valid:
        valid += 1
    else:
        invalid += 1
        errors.append((q['id'], msg))

print(f"Valid: {valid}, Invalid: {invalid}")
if errors:
    for e in errors[:5]:
        print(f"Error: {e}")
