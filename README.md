# NPTEL Management Information Systems (MIS) MCQ Question Bank Platform

A full-stack, enterprise-grade educational web application grounded in the complete 1,163-page source document **`MIS Week 1_merged.pdf`**.

---

## 🌟 Executive Summary & Exact MCQ Count

- **Total Validated MCQs:** **451** (Derived directly from SQLite database: `SELECT COUNT(*) FROM questions WHERE validation_status = 'VALIDATED'`).
- **Zero Guessed Targets:** The question total is the true number of validated, unique questions saved in the database.
- **Source Document Processed:** `MIS Week 1_merged.pdf` (1,163 pages total, 991 content slides across 60 lectures and 12 weeks).
- **Curriculum Architecture:** 12 Course Modules / Weeks, 60 Lectures, 3 Faculty Instructors (Prof. Surojit Mookherjee, Prof. Saini Das, Prof. Kunal Kanti Ghosh).
- **Validation Pipeline:** 100% of questions contain 4 options (A–D), a single unambiguous verified answer key, comprehensive explanation, distractor analysis, topic/subtopic, and slide page citations with quoted slide evidence.
- **Automated Consistency Check:** $\sum \text{Week-Wise MCQs} (451) \equiv \text{Overall Database MCQs} (451)$ — **Verified & Synchronized**.

---

## 🏛️ Website Layout & Organization (In Exact Requested Order)

### Section 1: Complete Question Bank — Overall Total
- **Prominent Top Display:** Exact validated count (`451`) rendered dynamically from the database.
- **Practice Tracking:** Live user metrics tracking questions answered correctly, incorrectly, accuracy percentage, and total attempts.
- **Pipeline Metrics:** Total PDF pages processed (`1,163`), content slides (`991`), detected weeks (`12`), lectures (`60`), completion status (`100% Complete`), pending review (`0`), and duplicate questions filtered (`3`).

### Section 2: Complete Week-Wise Question Count
- Comprehensive table listing all 12 weeks:
  | Week / Module | Topics and Lectures Covered | Validated MCQs | Status | Action |
  |---|---|---:|:---:|:---:|
  | **Week 1** | Intro to MIS, Digital Firm, Sociotechnical Systems (Lec 1–5, P1–90) | **65** | Complete | View / Practice |
  | **Week 2** | Foundations of Business Analytics & Database Systems (Lec 6–9, P91–160) | **46** | Complete | View / Practice |
  | **Week 3** | ERP Systems, BPR & Implementation (Lec 10–14, P161–225) | **39** | Complete | View / Practice |
  | **Week 4** | Enterprise Applications: CRM, SCM, SRM & PLM (Lec 15–19, P226–319) | **40** | Complete | View / Practice |
  | **Week 5** | Functional IS I: Manufacturing, Materials & Quality (Lec 20–24, P320–446) | **37** | Complete | View / Practice |
  | **Week 6** | Functional IS II: Marketing, Sales, Finance & HRM (Lec 25–29, P447–575) | **32** | Complete | View / Practice |
  | **Week 7** | IS Strategy, Balanced Scorecard & Cloud Architecture (Lec 30–34, P576–717) | **33** | Complete | View / Practice |
  | **Week 8** | E-Commerce: Digital Markets & Business Models (Lec 35–39, P718–783) | **30** | Complete | View / Practice |
  | **Week 9** | Emerging Technologies: Cloud, IoT, Big Data & Blockchain (Lec 40–45, P784–870) | **34** | Complete | View / Practice |
  | **Week 10** | Knowledge Management, DSS, ESS, Expert Systems & LMS (Lec 46–50, P871–1002) | **32** | Complete | View / Practice |
  | **Week 11** | Ethical, Social, Privacy & Cybersecurity Issues (Lec 51–55, P1003–1080) | **33** | Complete | View / Practice |
  | **Week 12** | Managing Global Organizations, SSO & Offshoring (Lec 56–60, P1081–1163) | **30** | Complete | View / Practice |
  | **TOTAL** | **All 12 Course Modules & 60 Lectures Grounded** | **451** | **100% Complete** | **View All** |
- **Automated Consistency Check Banner:** Confirms $\sum = 451$ matches database total with zero discrepancies.

### Section 3: Complete Question Bank — Every MCQ
- **Hierarchical Access:** Week $\rightarrow$ Module $\rightarrow$ Lecture $\rightarrow$ Topic $\rightarrow$ Individual MCQs.
- **Two Distinct Modes:**
  - **Mode A (Study and Learn):** Instant display of verified correct option, comprehensive explanations, distractor analysis, and direct slide quotation.
  - **Mode B (Test and Practice):** Interactive radio buttons, answers hidden until user clicks "Submit Answer", instant scoring feedback, progress updates, and anti-duplicate submission safeguards.
- **Filtering & Search:** Real-time text search across questions and explanations, Week dropdown, Lecture dropdown (all 60 lectures), Difficulty filter (Easy, Medium, Hard), Question Type filter (9 categories), and Bookmarks filter.
- **Pagination:** Smooth pagination supporting 10, 20, 50, 100, or All 451 questions per page.
- **Export Options:** One-click download of the complete bank in **JSON**, **CSV**, and **Print-Ready / Save as PDF**.

### Additional Features
- **Mock Exam Simulation Center:** Configurable timed exams (15, 25, or 50 questions) with live countdown timer, interactive question palette, submission, and instant scoring analytics.
- **Audit & Source Coverage Modal:** Transparency viewer documenting total pages (1,163), content slides (991), deduplication log, and validation metrics.

---

## 🚀 Running the Web Application

The application is powered by FastAPI and Uvicorn, serving the responsive frontend from `public/`:

```powershell
# 1. Start the server
python -m uvicorn server:app --host 127.0.0.1 --port 8000

# 2. Open in your browser
# URL: http://localhost:8000
```

### Automated Tests
Run the test suite to verify all endpoints and database consistency:
```powershell
python test_server_endpoints.py
```
