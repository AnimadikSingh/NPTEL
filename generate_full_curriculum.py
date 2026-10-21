# Comprehensive Full-Curriculum Question Bank Generation Engine
# Grounded strictly in MIS Week 1_merged.pdf across all 60 lectures and 12 weeks
# Targets ~125-135 high-quality, verified questions per week to reach 1,500+ MCQs

import sys
import os
import json
import importlib
import re

sys.stdout.reconfigure(encoding='utf-8')

from validator import validate_question

# Load base slide data
with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages_data = json.load(f)

with open("final_lectures.json", "r", encoding="utf-8") as f:
    lectures_data = json.load(f)

page_map = {p["page"]: p for p in pages_data}
lec_map = {l["id"]: l for l in lectures_data}

print(f"Loaded {len(pages_data)} pages, {len(lectures_data)} lectures.")
