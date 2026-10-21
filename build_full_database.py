# Comprehensive Question Bank Builder for NPTEL MIS Course
# Extracts and synthesizes verified questions for all 60 lectures across 12 weeks
# Directly grounded in MIS Week 1_merged.pdf

import json
import sqlite3
import re
import difflib
from validator import validate_question
from db import get_connection, init_database

# Import the existing handcrafted questions
from bank_generators.week01 import get_questions as get_w01
from bank_generators.week02 import get_questions as get_w02
from bank_generators.week03 import get_questions as get_w03
from bank_generators.week04 import get_questions as get_w04
from bank_generators.week05 import get_questions as get_w05
from bank_generators.week06 import get_questions as get_w06
from bank_generators.week07 import get_questions as get_w07
from bank_generators.week08 import get_questions as get_w08
from bank_generators.week09 import get_questions as get_w09
from bank_generators.week10 import get_questions as get_w10
from bank_generators.week11 import get_questions as get_w11
from bank_generators.week12 import get_questions as get_w12

def collect_curated_questions():
    all_q = []
    all_q.extend(get_w01())
    all_q.extend(get_w02())
    all_q.extend(get_w03())
    all_q.extend(get_w04())
    all_q.extend(get_w05())
    all_q.extend(get_w06())
    all_q.extend(get_w07())
    all_q.extend(get_w08())
    all_q.extend(get_w09())
    all_q.extend(get_w10())
    all_q.extend(get_w11())
    all_q.extend(get_w12())
    return all_q

if __name__ == "__main__":
    init_database()
    curated = collect_curated_questions()
    print(f"Base curated questions count: {len(curated)}")
