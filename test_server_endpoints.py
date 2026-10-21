import sys
sys.stdout.reconfigure(encoding='utf-8')

from starlette.testclient import TestClient
from server import app

client = TestClient(app)

def test_endpoints():
    print("Testing /api/stats...")
    r = client.get("/api/stats")
    assert r.status_code == 200, f"Stats failed: {r.status_code}"
    stats = r.json()
    print(f"Stats OK: Total Validated MCQs = {stats['total_validated_mcqs']}")
    assert stats['total_validated_mcqs'] == 1560, f"Expected 1560, got {stats['total_validated_mcqs']}"
    assert stats['total_weeks_detected'] == 12
    assert stats['total_lectures_detected'] == 60
    assert stats['total_pages_processed'] == 1163

    print("\nTesting /api/weeks...")
    r = client.get("/api/weeks")
    assert r.status_code == 200, f"Weeks failed: {r.status_code}"
    weeks_data = r.json()
    print(f"Weeks OK: {len(weeks_data['weeks'])} weeks returned")
    assert len(weeks_data['weeks']) == 12
    assert weeks_data['consistency_check_passed'] == True
    assert weeks_data['sum_of_week_mcqs'] == 1560
    assert weeks_data['overall_database_total'] == 1560

    print("\nTesting /api/questions...")
    r = client.get("/api/questions?page=1&limit=5")
    assert r.status_code == 200, f"Questions failed: {r.status_code}"
    q_data = r.json()
    print(f"Questions OK: {q_data['total']} total, {len(q_data['questions'])} returned on page 1")
    assert q_data['total'] == 1560
    assert len(q_data['questions']) == 5

    # Check question structure
    sample_q = q_data['questions'][0]
    required_keys = [
        "id", "week", "lecture_id", "question", "option_a", "option_b", "option_c", "option_d",
        "correct_answer", "explanation", "source_page", "source_evidence", "difficulty", "question_type"
    ]
    for k in required_keys:
        assert k in sample_q, f"Missing key {k} in question"
    print(f"Sample Question Verified: {sample_q['id']} - Correct Answer: {sample_q['correct_answer']}")

    print("\nTesting Practice Submission...")
    r = client.post("/api/practice/submit", json={
        "question_id": sample_q["id"],
        "selected_option": sample_q["correct_answer"],
        "mode": "test"
    })
    assert r.status_code == 200
    res = r.json()
    assert res["is_correct"] == True
    print(f"Practice submit OK: is_correct={res['is_correct']}")

    print("\nTesting /api/export/json...")
    r = client.get("/api/export/json")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/json"
    print(f"JSON export OK: {len(r.content)} bytes")

    print("\nTesting /api/export/csv...")
    r = client.get("/api/export/csv")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    print(f"CSV export OK: {len(r.content)} bytes")

    print("\nTesting /api/export/printable...")
    r = client.get("/api/export/printable")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Total Validated MCQs: 1560" in r.text
    print(f"Printable HTML export OK: {len(r.text)} characters")

    print("\nTesting / (frontend index.html)...")
    r = client.get("/")
    assert r.status_code == 200
    assert "NPTEL MIS Question Bank" in r.text
    print("Frontend index.html loads OK!")

    print("\nTesting /view.html...")
    r = client.get("/view.html?week=all")
    assert r.status_code == 200
    assert "Study &amp; View Mode" in r.text or "View Mode" in r.text
    print("view.html loads OK!")

    print("\nTesting /practice.html...")
    r = client.get("/practice.html?week=1")
    assert r.status_code == 200
    assert "Practice Mode" in r.text
    print("practice.html loads OK!")

    print("\nTesting /pdf-viewer.html...")
    r = client.get("/pdf-viewer.html")
    assert r.status_code == 200
    assert "MIS Week 1_merged.pdf" in r.text
    print("pdf-viewer.html loads OK!")

    print("\nTesting /MIS_Week_1_merged.pdf...")
    r = client.get("/MIS_Week_1_merged.pdf")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert len(r.content) == 9860298
    print(f"Source PDF served OK: {len(r.content)} bytes (9.8 MB)")

    print("\nALL 12 ENDPOINT & MULTI-PAGE TESTS PASSED SUCCESSFULLY! 100% VALID.")

if __name__ == "__main__":
    test_endpoints()
