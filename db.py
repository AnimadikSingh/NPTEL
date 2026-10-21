import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mis_questions.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Tables:
    # 1. weeks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weeks (
        week_num INTEGER PRIMARY KEY,
        week_title TEXT NOT NULL,
        topics_summary TEXT,
        total_lectures INTEGER NOT NULL,
        start_page INTEGER NOT NULL,
        end_page INTEGER NOT NULL,
        status TEXT DEFAULT 'Completed'
    )
    """)

    # 2. lectures
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lectures (
        id TEXT PRIMARY KEY,
        lecture_index INTEGER NOT NULL,
        week_num INTEGER NOT NULL,
        lecture_num INTEGER NOT NULL,
        title TEXT NOT NULL,
        instructor TEXT NOT NULL,
        start_page INTEGER NOT NULL,
        end_page INTEGER NOT NULL,
        page_count INTEGER NOT NULL,
        FOREIGN KEY (week_num) REFERENCES weeks (week_num)
    )
    """)

    # 3. questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        week INTEGER NOT NULL,
        week_title TEXT NOT NULL,
        lecture_id TEXT NOT NULL,
        lecture_num INTEGER NOT NULL,
        lecture_title TEXT NOT NULL,
        topic TEXT NOT NULL,
        subtopic TEXT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        explanation TEXT NOT NULL,
        distractor_explanations TEXT,
        source_page INTEGER NOT NULL,
        source_evidence TEXT NOT NULL,
        question_type TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        validation_status TEXT DEFAULT 'VALIDATED',
        rejection_reason TEXT,
        is_duplicate INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (week) REFERENCES weeks (week_num),
        FOREIGN KEY (lecture_id) REFERENCES lectures (id)
    )
    """)

    # 4. user_answers (tracking practice and mock tests)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id TEXT NOT NULL,
        selected_option TEXT NOT NULL,
        is_correct INTEGER NOT NULL,
        mode TEXT NOT NULL,
        test_session_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    """)

    # 5. bookmarks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        question_id TEXT PRIMARY KEY,
        note TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    """)

    # 6. mock_tests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_tests (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        week_filter TEXT,
        total_questions INTEGER NOT NULL,
        score INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        incorrect_count INTEGER NOT NULL,
        unanswered_count INTEGER NOT NULL,
        accuracy_percent REAL NOT NULL,
        time_spent_seconds INTEGER NOT NULL,
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. audit_stats
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        details TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_week ON questions(week);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_lecture ON questions(lecture_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_status ON questions(validation_status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic);")

    conn.commit()

    # Populate weeks and lectures from final_lectures.json
    if os.path.exists("final_lectures.json"):
        with open("final_lectures.json", "r", encoding="utf-8") as f:
            lectures = json.load(f)

        # Build week summaries
        weeks_map = {}
        for l in lectures:
            w = l["week_num"]
            if w not in weeks_map:
                weeks_map[w] = {
                    "week_num": w,
                    "week_title": l["week_title"],
                    "lectures": [],
                    "start_page": l["start_page"],
                    "end_page": l["end_page"]
                }
            weeks_map[w]["lectures"].append(l)
            weeks_map[w]["end_page"] = max(weeks_map[w]["end_page"], l["end_page"])

        for w, data in weeks_map.items():
            topics_summary = ", ".join([lec["title"] for lec in data["lectures"]])
            cursor.execute("""
            INSERT OR REPLACE INTO weeks (week_num, week_title, topics_summary, total_lectures, start_page, end_page, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (w, data["week_title"], topics_summary, len(data["lectures"]), data["start_page"], data["end_page"], "Complete"))

        for l in lectures:
            cursor.execute("""
            INSERT OR REPLACE INTO lectures (id, lecture_index, week_num, lecture_num, title, instructor, start_page, end_page, page_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (l["id"], l["index"], l["week_num"], l["lecture_num"], l["title"], l["instructor"], l["start_page"], l["end_page"], l["page_count"]))

        conn.commit()

    conn.close()
    print("Database initialized successfully at", DB_PATH)

if __name__ == "__main__":
    init_database()
