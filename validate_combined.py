import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

from validator import validate_question
import gen_weeks_1_3, gen_weeks_4_6, gen_weeks_7_9, gen_weeks_10_12

bg = []
for w in range(1, 13):
    mod = importlib.import_module(f'bank_generators.week{w:02d}')
    bg.extend(mod.get_questions())

gw = []
gw.extend(gen_weeks_1_3.get_questions_w1_w3())
gw.extend(gen_weeks_4_6.get_questions_w4_w6())
gw.extend(gen_weeks_7_9.get_questions_w7_w9())
gw.extend(gen_weeks_10_12.get_questions_w10_w12())

# Combine and ensure unique IDs
combined = []
seen_texts = set()
for q in bg:
    t = q['question'].strip().lower()
    if t not in seen_texts:
        seen_texts.add(t)
        combined.append(q)

for q in gw:
    t = q['question'].strip().lower()
    if t not in seen_texts:
        seen_texts.add(t)
        # Give unique ID if duplicated
        combined.append(q)

# Re-assign clean unique IDs so there are no collisions
for idx, q in enumerate(combined, 1):
    w = q.get('week', 1)
    lid = q.get('lecture_id', 'LEC-01')
    q['id'] = f"MIS-W{w:02d}-{lid}-{idx:04d}"

valid_count = 0
invalid_count = 0
errors = []

for q in combined:
    is_valid, msg = validate_question(q)
    if is_valid:
        valid_count += 1
    else:
        invalid_count += 1
        errors.append((q['id'], msg))

print(f"Total Combined Questions Tested: {len(combined)}")
print(f"Valid: {valid_count}")
print(f"Invalid: {invalid_count}")
if errors:
    print("\nErrors:")
    for eid, err in errors[:10]:
        print(f"  {eid}: {err}")
