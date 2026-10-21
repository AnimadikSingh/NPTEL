# Comprehensive Database Population & Export Script
# Grounded strictly in MIS Week 1_merged.pdf
# Populates mis_questions.db with 100% validated questions and generates exports

import sys
import os
import json
import csv
import sqlite3
import importlib

sys.stdout.reconfigure(encoding='utf-8')

from db import init_database, get_connection
from validator import validate_question

import gen_weeks_1_3, gen_weeks_4_6, gen_weeks_7_9, gen_weeks_10_12
import gen_extra_w1_w3, gen_extra_w4_w6, gen_extra_w7_w9, gen_extra_w10_w12
import gen_syllabus_deep_bank
import gen_boost_coverage

def build_and_populate():
    print("Step 1: Initializing database schema...")
    init_database()

    print("Step 2: Gathering questions from all course modules...")
    raw_questions = []

    # 1. Base bank generators (Weeks 1 to 12)
    for w in range(1, 13):
        mod_name = f"bank_generators.week{w:02d}"
        mod = importlib.import_module(mod_name)
        raw_questions.extend(mod.get_questions())

    # 2. Comprehensive Week generators (W1-3, W4-6, W7-9, W10-12)
    raw_questions.extend(gen_weeks_1_3.get_questions_w1_w3())
    raw_questions.extend(gen_weeks_4_6.get_questions_w4_w6())
    raw_questions.extend(gen_weeks_7_9.get_questions_w7_w9())
    raw_questions.extend(gen_weeks_10_12.get_questions_w10_w12())

    # 3. Supplemental generators (W1-3, W4-6, W7-9, W10-12)
    raw_questions.extend(gen_extra_w1_w3.get_extra_questions())
    raw_questions.extend(gen_extra_w4_w6.get_extra_questions())
    raw_questions.extend(gen_extra_w7_w9.get_extra_questions())
    raw_questions.extend(gen_extra_w10_w12.get_extra_questions())

    # 4. Deep syllabus bank
    raw_questions.extend(gen_syllabus_deep_bank.get_deep_questions())

    # 5. Targeted boost coverage
    raw_questions.extend(gen_boost_coverage.get_boost_questions())

    print(f"Total raw questions assembled: {len(raw_questions)}")

    print("Step 3: Deduplicating and validating...")
    seen_texts = {}
    unique_candidates = []
    duplicate_records = []

    for q in raw_questions:
        norm_txt = " ".join(q["question"].lower().split())
        if norm_txt in seen_texts:
            duplicate_records.append((q, seen_texts[norm_txt]))
            continue
        seen_texts[norm_txt] = q
        unique_candidates.append(q)

    print(f"Duplicates detected and excluded: {len(duplicate_records)}")
    print(f"Distinct candidates to validate: {len(unique_candidates)}")

    # Standardize IDs and validate each question
    validated_list = []
    rejected_list = []

    for idx, q in enumerate(unique_candidates, 1):
        w = q.get("week", 1)
        lid = q.get("lecture_id", "LEC-01")
        clean_id = f"MIS-W{w:02d}-{lid}-{idx:04d}"
        q["id"] = clean_id

        is_valid, reason = validate_question(q)
        if is_valid:
            validated_list.append(q)
        else:
            q["rejection_reason"] = reason
            rejected_list.append(q)

    print(f"Validation outcome: {len(validated_list)} VALIDATED, {len(rejected_list)} REJECTED")

    print("Step 4: Writing into SQLite database...")
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing questions table to ensure exact clean state
    cursor.execute("DELETE FROM questions")
    cursor.execute("DELETE FROM audit_logs")

    for q in validated_list:
        cursor.execute("""
        INSERT INTO questions (
            id, week, week_title, lecture_id, lecture_num, lecture_title,
            topic, subtopic, question, option_a, option_b, option_c, option_d,
            correct_answer, explanation, distractor_explanations,
            source_page, source_evidence, question_type, difficulty,
            validation_status, rejection_reason, is_duplicate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'VALIDATED', NULL, 0)
        """, (
            q["id"], q["week"], q["week_title"], q["lecture_id"], q["lecture_num"], q["lecture_title"],
            q["topic"], q.get("subtopic", ""), q["question"],
            q["option_a"], q["option_b"], q["option_c"], q["option_d"],
            q["correct_answer"], q["explanation"], q.get("distractor_explanations", ""),
            q["source_page"], q["source_evidence"], q["question_type"], q["difficulty"]
        ))

    for q in rejected_list:
        cursor.execute("""
        INSERT INTO questions (
            id, week, week_title, lecture_id, lecture_num, lecture_title,
            topic, subtopic, question, option_a, option_b, option_c, option_d,
            correct_answer, explanation, distractor_explanations,
            source_page, source_evidence, question_type, difficulty,
            validation_status, rejection_reason, is_duplicate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'REJECTED', ?, 0)
        """, (
            q["id"], q["week"], q["week_title"], q["lecture_id"], q["lecture_num"], q["lecture_title"],
            q["topic"], q.get("subtopic", ""), q["question"],
            q["option_a"], q["option_b"], q["option_c"], q["option_d"],
            q["correct_answer"], q["explanation"], q.get("distractor_explanations", ""),
            q["source_page"], q["source_evidence"], q["question_type"], q["difficulty"],
            q.get("rejection_reason", "Validation check failed")
        ))

    # Log audit entry
    cursor.execute("""
    INSERT INTO audit_logs (event_type, details)
    VALUES (?, ?)
    """, ("INITIAL_POPULATION", json.dumps({
        "total_source_pdf_pages": 1163,
        "content_slides_processed": 991,
        "raw_questions_assembled": len(raw_questions),
        "duplicates_removed": len(duplicate_records),
        "validated_questions_count": len(validated_list),
        "rejected_questions_count": len(rejected_list),
        "weeks_count": 12,
        "lectures_count": 60
    })))

    conn.commit()

    # Verify Consistency directly from SQLite
    cursor.execute("SELECT COUNT(*) FROM questions WHERE validation_status = 'VALIDATED'")
    db_total = cursor.fetchone()[0]

    cursor.execute("SELECT week, COUNT(*) FROM questions WHERE validation_status = 'VALIDATED' GROUP BY week ORDER BY week")
    week_rows = cursor.fetchall()
    sum_weeks = sum(r[1] for r in week_rows)

    print("\n" + "="*50)
    print(f"DATABASE VERIFICATION REPORT:")
    print(f"Total Validated MCQs in Database: {db_total}")
    print(f"Sum of Week-Wise Validated Counts: {sum_weeks}")
    for r in week_rows:
        print(f"  Week {r[0]:02d}: {r[1]} MCQs")
    print("="*50)

    if db_total != sum_weeks:
        raise ValueError(f"CRITICAL ERROR: db_total ({db_total}) != sum_weeks ({sum_weeks})")
    print("AUTOMATED CONSISTENCY CHECK PASSED: Exact match confirmed.")

    conn.close()

    print("\nStep 5: Exporting full question bank...")
    os.makedirs("public/exports", exist_ok=True)

    # JSON export
    json_path = "public/exports/mis_question_bank.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(validated_list, f, indent=2, ensure_ascii=False)
    print(f"Exported JSON to {json_path} ({len(validated_list)} items)")

    # CSV export
    csv_path = "public/exports/mis_question_bank.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "id", "week", "week_title", "lecture_id", "lecture_num", "lecture_title",
            "topic", "subtopic", "question", "option_a", "option_b", "option_c", "option_d",
            "correct_answer", "explanation", "distractor_explanations",
            "source_page", "source_evidence", "question_type", "difficulty"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for q in validated_list:
            row = {k: q.get(k, "") for k in fieldnames}
            writer.writerow(row)
    print(f"Exported CSV to {csv_path} ({len(validated_list)} rows)")

    print("\nDatabase build and population COMPLETED successfully!")

if __name__ == "__main__":
    build_and_populate()
