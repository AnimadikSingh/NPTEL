from gen_weeks_1_3 import get_questions_w1_w3
from validator import validate_question

qs = get_questions_w1_w3()
print(f"Validating {len(qs)} questions...")
all_valid = True
existing = []
for q in qs:
    v, errs = validate_question(q, existing)
    if not v:
        print(f"FAIL {q['id']}: {errs}")
        all_valid = False
    existing.append(q)

if all_valid:
    print("ALL QUESTIONS PASSED VALIDATION PERFECTLY!")
