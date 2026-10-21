import sys
import importlib
import json

sys.stdout.reconfigure(encoding='utf-8')

import gen_weeks_1_3
import gen_weeks_4_6
import gen_weeks_7_9
import gen_weeks_10_12

bg = []
for w in range(1, 13):
    mod = importlib.import_module(f'bank_generators.week{w:02d}')
    bg.extend(mod.get_questions())

gw = []
gw.extend(gen_weeks_1_3.get_questions_w1_w3())
gw.extend(gen_weeks_4_6.get_questions_w4_w6())
gw.extend(gen_weeks_7_9.get_questions_w7_w9())
gw.extend(gen_weeks_10_12.get_questions_w10_w12())

print(f"BG count: {len(bg)}, GW count: {len(gw)}")

texts_bg = {q['question'].strip().lower(): q for q in bg}
overlap = 0
for q in gw:
    t = q['question'].strip().lower()
    if t in texts_bg:
        overlap += 1

print(f"Text overlap: {overlap}")
