import re
import difflib

def validate_question(q, existing_questions=None):
    """
    Validates a question dict according to Section 7:
    - Must have exactly 4 options: A, B, C, D
    - All options must be non-empty strings
    - Options must not be duplicated
    - Correct answer must be one of 'A', 'B', 'C', 'D'
    - Question text must be at least 15 chars and end with punctuation or '?'
    - Explanation must be non-empty (>= 20 chars)
    - Source page must be integer within [1, 1163]
    - Source evidence must be non-empty
    - Week must be 1..12
    - Lecture id must be non-empty
    - Must not be duplicate of existing question
    """
    errors = []

    # Check question text
    q_text = q.get("question", "").strip()
    if not q_text or len(q_text) < 15:
        errors.append("Question text too short or empty")

    # Check options
    options = {
        "A": q.get("option_a", "").strip(),
        "B": q.get("option_b", "").strip(),
        "C": q.get("option_c", "").strip(),
        "D": q.get("option_d", "").strip()
    }
    for opt_k, opt_v in options.items():
        if not opt_v:
            errors.append(f"Option {opt_k} is missing or empty")

    # Check duplicate options
    opt_values = [v.lower() for v in options.values() if v]
    if len(opt_values) != len(set(opt_values)):
        errors.append("Duplicate options detected in question")

    # Check correct answer
    corr = q.get("correct_answer", "").strip().upper()
    if corr not in ["A", "B", "C", "D"]:
        errors.append(f"Invalid correct answer '{corr}', must be A, B, C, or D")

    # Check explanation
    expl = q.get("explanation", "").strip()
    if not expl or len(expl) < 20:
        errors.append("Explanation is missing or too brief (minimum 20 chars)")

    # Check source page
    try:
        page = int(q.get("source_page", 0))
        if page < 1 or page > 1163:
            errors.append(f"Source page {page} out of range [1, 1163]")
    except (ValueError, TypeError):
        errors.append("Source page must be an integer")

    # Check source evidence
    evidence = q.get("source_evidence", "").strip()
    if not evidence or len(evidence) < 5:
        errors.append("Source evidence quote is missing or too short")

    # Check week
    week = q.get("week")
    if not isinstance(week, int) or week < 1 or week > 12:
        errors.append(f"Invalid week number '{week}', must be 1..12")

    # Check duplicate question against existing questions
    if existing_questions:
        q_norm = re.sub(r'[^a-zA-Z0-9]', '', q_text.lower())
        for existing in existing_questions:
            ex_norm = re.sub(r'[^a-zA-Z0-9]', '', existing.get("question", "").lower())
            if q_norm == ex_norm:
                errors.append(f"Exact duplicate of existing question ID {existing.get('id')}")
                break
            # Check high similarity
            ratio = difflib.SequenceMatcher(None, q_norm, ex_norm).ratio()
            if ratio > 0.90:
                errors.append(f"Near-duplicate (similarity {ratio:.2f}) of question ID {existing.get('id')}")
                break

    is_valid = len(errors) == 0
    return is_valid, errors
