import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

from validator import validate_question
import gen_weeks_1_3, gen_weeks_4_6, gen_weeks_7_9, gen_weeks_10_12
import gen_extra_w1_w3, gen_extra_w4_w6, gen_extra_w7_w9, gen_extra_w10_w12
import gen_syllabus_deep_bank

sources = []

# Source 1: bank_generators (Week 1 to 12)
for w in range(1, 13):
    mod = importlib.import_module(f'bank_generators.week{w:02d}')
    sources.extend(mod.get_questions())

# Source 2: gen_weeks (W1-3, W4-6, W7-9, W10-12)
sources.extend(gen_weeks_1_3.get_questions_w1_w3())
sources.extend(gen_weeks_4_6.get_questions_w4_w6())
sources.extend(gen_weeks_7_9.get_questions_w7_w9())
sources.extend(gen_weeks_10_12.get_questions_w10_w12())

# Source 3: gen_extra (W1-3, W4-6, W7-9, W10-12)
sources.extend(gen_extra_w1_w3.get_extra_questions())
sources.extend(gen_extra_w4_w6.get_extra_questions())
sources.extend(gen_extra_w7_w9.get_extra_questions())
sources.extend(gen_extra_w10_w12.get_extra_questions())

# Source 4: gen_syllabus_deep_bank
sources.extend(gen_syllabus_deep_bank.get_deep_questions())

print(f"Total raw questions pulled from all sources: {len(sources)}")

# Deduplicate strictly on question text
unique_questions = []
seen = set()
duplicates_found = 0

for q in sources:
    text_norm = " ".join(q["question"].lower().split())
    if text_norm in seen:
        duplicates_found += 1
        continue
    seen.add(text_norm)
    unique_questions.append(q)

print(f"Duplicates removed: {duplicates_found}")
print(f"Unique questions count: {len(unique_questions)}")

# Assign clean standard IDs and validate
valid_questions = []
rejected_questions = []

for idx, q in enumerate(unique_questions, 1):
    w = q.get("week", 1)
    lid = q.get("lecture_id", "LEC-01")
    q["id"] = f"MIS-W{w:02d}-{lid}-{idx:04d}"
    
    is_valid, err = validate_question(q)
    if is_valid:
        valid_questions.append(q)
    else:
        rejected_questions.append((q, err))

print(f"Validation summary: {len(valid_questions)} VALID, {len(rejected_questions)} REJECTED")

# Check week-wise counts
week_counts = {}
for q in valid_questions:
    w = q["week"]
    week_counts[w] = week_counts.get(w, 0) + 1

print("\nWeek-wise breakdown:")
for w in sorted(week_counts.keys()):
    print(f"  Week {w:02d}: {week_counts[w]} questions")

total_from_weeks = sum(week_counts.values())
print(f"\nSum of all week counts: {total_from_weeks}")
print(f"Total validated questions: {len(valid_questions)}")
assert total_from_weeks == len(valid_questions), "Week consistency check failed!"
print("Consistency check PASSED: sum(week_counts) == total_validated_questions")
