import sqlite3
import json

conn = sqlite3.connect('mis_questions.db')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM questions WHERE validation_status = 'VALIDATED'")
total = c.fetchone()[0]
print(f"Total validated questions in mis_questions.db: {total}")

c.execute("SELECT week, COUNT(*) FROM questions WHERE validation_status = 'VALIDATED' GROUP BY week ORDER BY week")
rows = c.fetchall()
for r in rows:
    print(f"Week {r[0]:02d}: {r[1]} questions")

conn.close()
