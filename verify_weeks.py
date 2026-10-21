import json
import re

with open("extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

with open("curated_lectures.json", "r", encoding="utf-8") as f:
    lectures = json.load(f)

# Let's clean up lecture titles and organize weeks cleanly
# We know there are 12 weeks:
# Week 1: Lectures 1-5 (Intro to MIS, Dimensions, Digital Firm, Laudon Ch 1)
# Week 2: Lectures 6-9 (Databases & Info Mgmt, Data Warehouses & BI, Data Mining, Analytics Tools)
# Week 3: Lectures 10-14 (ERP Overview, Evolution & Benefits, Advantages, Risks & Challenges, BPR)
# Week 4: Lectures 15-19 (CRM, SCM Part 1, SCM Part 2, SRM, PLM)
# Week 5: Lectures 20-24 (Manufacturing IS 1 & 2, Materials Mgmt IS, Quality Mgmt IS, Marketing IS Part 1)
# Week 6: Lectures 25-29 (Marketing IS Part 2, Sales & Distribution IS, Finance & Accounting IS, HRM IS Part 1 & 2)
# Week 7: Lectures 30-34 (IS Strategy, Aligning IT with Business Objectives, Balanced Score Card, Data Centers & Virtualization, Selection of Cloud Vendor)
# Week 8: Lectures 35-39 (E-commerce Intro, B2C Models, B2B Models, Unique E-commerce Models, Social & M-commerce)
# Week 9: Lectures 40-45 (Cloud Computing I & II, IoT I, II, III, Big Data & Emerging Tech)
# Week 10: Lectures 46-50 (KMS, DSS, ESS, Expert Systems, LMS)
# Week 11: Lectures 51-55 (Ethical & Social Issues I & II, Security Issues I, II & III)
# Week 12: Lectures 56-60 (Managing Global Organizations I & II, Shared Services, Offshoring/Transitioning IT Systems, Flat World Globalization)

week_mapping = {
    1: {"title": "Introduction to MIS & The Digital Firm", "lectures": [1, 2, 3, 4, 5]},
    2: {"title": "Foundations of Business Analytics & Database Systems", "lectures": [6, 7, 8, 9]},
    3: {"title": "Enterprise Resource Planning (ERP) Systems & BPR", "lectures": [10, 11, 12, 13, 14]},
    4: {"title": "Enterprise Applications (CRM, SCM, SRM, PLM)", "lectures": [15, 16, 17, 18, 19]},
    5: {"title": "Functional Information Systems I (Manufacturing, Materials, Quality, Marketing)", "lectures": [20, 21, 22, 23, 24]},
    6: {"title": "Functional Information Systems II (Sales & Distribution, Finance, Accounting, HRM)", "lectures": [25, 26, 27, 28, 29]},
    7: {"title": "Information Systems Strategy, Balanced Scorecard & Cloud Architecture", "lectures": [30, 31, 32, 33, 34]},
    8: {"title": "E-Commerce: Digital Markets, B2C/B2B Business Models & Digital Goods", "lectures": [35, 36, 37, 38, 39]},
    9: {"title": "Emerging Technologies: Cloud Computing, IoT, Big Data & Blockchain", "lectures": [40, 41, 42, 43, 44, 45]},
    10: {"title": "Knowledge Management, DSS, ESS, Expert Systems & LMS", "lectures": [46, 47, 48, 49, 50]},
    11: {"title": "Ethical, Social, Privacy & Cybersecurity Issues in MIS", "lectures": [51, 52, 53, 54, 55]},
    12: {"title": "Managing Global Organizations, Shared Services & IT Offshoring", "lectures": [56, 57, 58, 59, 60]}
}

print("Week mapping created successfully.")
