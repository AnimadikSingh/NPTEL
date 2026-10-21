import importlib
import json

total = 0
weeks_count = {}

for w in range(1, 13):
    mod_name = f"bank_generators.week{w:02d}"
    try:
        mod = importlib.import_module(mod_name)
        qs = mod.get_questions()
        total += len(qs)
        weeks_count[w] = len(qs)
        print(f"Week {w:02d}: {len(qs)} questions")
    except Exception as e:
        print(f"Week {w:02d}: Error {e}")

print(f"Total across all available generators: {total}")
