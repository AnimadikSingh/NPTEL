import json
import re

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

# Let's inspect slide patterns
definitions = []
lists = []
examples = []

for p in pages:
    p_num = p["page"]
    lines = p["lines"]
    txt = " ".join(lines)
    
    # Check for definition pattern
    for line in lines:
        if any(term in line.lower() for term in ["is defined as", "is a set of", "refers to", "describes how", "consists of"]):
            definitions.append((p_num, line))
        if any(term in line.lower() for term in ["e.g.", "for example", "such as", "examples:"]):
            examples.append((p_num, line))
        if re.search(r'^\d+\.\s+[A-Z]', line) or re.search(r'^[•\-\*]\s+[A-Z]', line):
            lists.append((p_num, line))

print(f"Extracted {len(definitions)} definition lines, {len(examples)} example lines, {len(lists)} list items.")
print("\nSample Definitions:")
for p, d in definitions[:10]:
    print(f"P{p}: {d}")
print("\nSample Examples:")
for p, e in examples[:10]:
    print(f"P{p}: {e}")
