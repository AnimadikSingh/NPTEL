import json

with open("markers.json", "r", encoding="utf-8") as f:
    markers = json.load(f)

print(f"Total markers: {len(markers)}")
for m in markers:
    p = m["page"]
    lines = " | ".join(m["lines"])
    print(f"P.{p:4d}: {lines[:100]}")
