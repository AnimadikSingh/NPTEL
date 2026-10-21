import json
import re

with open("curated_lectures.json", "r", encoding="utf-8") as f:
    curated = json.load(f)

# Clean up lecture titles and metadata
clean_lectures = []

week_names = {
    1: "Introduction to MIS & The Digital Firm",
    2: "Foundations of Business Analytics & Database Systems",
    3: "Enterprise Resource Planning (ERP) Systems & BPR",
    4: "Enterprise Applications: CRM, SCM, SRM & PLM",
    5: "Functional Information Systems I: Manufacturing, Materials & Quality",
    6: "Functional Information Systems II: Marketing, Sales, Finance & HRM",
    7: "IS Strategy, Balanced Scorecard & Cloud Architecture",
    8: "E-Commerce: Digital Markets, Business Models & Goods",
    9: "Emerging Technologies: Cloud, IoT, Big Data & Blockchain",
    10: "Knowledge Management, DSS, ESS, Expert Systems & LMS",
    11: "Ethical, Social, Privacy & Cybersecurity Issues in MIS",
    12: "Managing Global Organizations, Shared Services & Offshoring"
}

title_overrides = {
    1: "Introduction to MIS - Part 1",
    2: "Introduction to MIS - Part 2",
    3: "Dimensions of Information Systems (Org, Mgmt, Tech)",
    4: "Information Management in the Digital World",
    5: "Class Discussions & Case Synthesis",
    6: "Databases & Information Management",
    7: "Data Warehouses & Business Intelligence",
    8: "Introduction to Data Mining & KDD Process",
    9: "Data Analytics Tools and Techniques",
    10: "Overview and Definition of ERP",
    11: "Evolution of ERP (MRP, Closed-Loop, MRP II, ERP)",
    12: "Advantages & Business Benefits of ERP",
    13: "Risks and Challenges of ERP Implementation",
    14: "ERP Implementation Methodology & Discussion",
    15: "Customer Relationship Management (CRM) Architecture",
    16: "Supply Chain Management (SCM) - Core Concepts",
    17: "Supply Chain Management - Bullwhip Effect & Push vs Pull",
    18: "Supplier Relationship Management (SRM) & E-Procurement",
    19: "Product Lifecycle Management (PLM) Systems",
    20: "IS for Manufacturing Management - Planning & Control",
    21: "IS for Manufacturing Management - CAD & Additive Mfg",
    22: "IS for Materials Management (MM) & MRP explosion",
    23: "IS for Quality Management (QM) & Statistical Process Control",
    24: "Marketing Information Systems (MKIS) - Part 1",
    25: "Marketing Information Systems (MKIS) - Research & Intelligence",
    26: "Sales & Distribution Information Systems (SDIS)",
    27: "Financial & Accounting Information Systems (FMIS)",
    28: "Human Resource Information Systems (HRIS) - Part 1",
    29: "Human Resource Information Systems (HRIS) - Part 2",
    30: "Information Systems (IS) Strategy & Competitive Forces",
    31: "Aligning IT with Strategic Business Objectives",
    32: "Balanced Scorecard (BSC) Framework & KPIs",
    33: "Data Centers, Virtualization & Server Consolidation",
    34: "Selection of Cloud Vendor & Cloud Service Level Agreements",
    35: "Introduction to E-Commerce & Digital Markets",
    36: "B2C Business Models (Portal, E-tailer, Content, Broker)",
    37: "B2B Business Models & Electronic Marketplaces",
    38: "Unique E-Commerce Models (Auctions, Crowdfunding, Flash Deals)",
    39: "Social Commerce, M-Commerce & Location-Based Services",
    40: "Cloud Computing Architectures & XaaS Models - Part 1",
    41: "Cloud Computing Deployment Models & SLAs - Part 2",
    42: "Internet of Things (IoT) - Architecture & Sensors - Part 1",
    43: "Internet of Things (IoT) - Industrial & Urban Applications - Part 2",
    44: "Internet of Things (IoT) - Challenges & Privacy by Design - Part 3",
    45: "Big Data (4Vs) & Blockchain Technology",
    46: "Knowledge Management Systems (KMS) & Value Chain",
    47: "Decision Support Systems (DSS) - Models & What-If Analysis",
    48: "Executive Support Systems (ESS) & Digital Dashboards",
    49: "Expert Systems & AI Knowledge Representation",
    50: "Learning Management Systems (LMS) & MOODLE",
    51: "Ethical and Social Issues in Information Systems - Part 1",
    52: "Privacy Laws & Regulations (HIPAA, FIP, GDPR) - Part 2",
    53: "Cybersecurity Threats & Malware (Viruses, Worms, Ransomware)",
    54: "Cyber Attacks, Identity Theft, Phishing & Pharming",
    55: "Security Solutions, Defense-in-Depth, UTM & Computer Forensics",
    56: "Managing Global Organizations - Globalization Drivers",
    57: "Global Strategies & International IS Architectures",
    58: "Shared Services Organization & Delivery Models",
    59: "Offshoring, Transitioning & Knowledge Transfer (KT)",
    60: "Globalization of Corporates in a Flat World (Thomas Friedman's 10 Flatteners)"
}

for c in curated:
    idx = c["index"]
    w_num = c["week_num"]
    # fix week num if needed:
    if 1 <= idx <= 5:
        w_num = 1
    elif 6 <= idx <= 9:
        w_num = 2
    elif 10 <= idx <= 14:
        w_num = 3
    elif 15 <= idx <= 19:
        w_num = 4
    elif 20 <= idx <= 24:
        w_num = 5
    elif 25 <= idx <= 29:
        w_num = 6
    elif 30 <= idx <= 34:
        w_num = 7
    elif 35 <= idx <= 39:
        w_num = 8
    elif 40 <= idx <= 45:
        w_num = 9
    elif 46 <= idx <= 50:
        w_num = 10
    elif 51 <= idx <= 55:
        w_num = 11
    elif 56 <= idx <= 60:
        w_num = 12

    lec_num = idx - min([x["index"] for x in curated if (
        1 <= idx <= 5 and 1 <= x["index"] <= 5 or
        6 <= idx <= 9 and 6 <= x["index"] <= 9 or
        10 <= idx <= 14 and 10 <= x["index"] <= 14 or
        15 <= idx <= 19 and 15 <= x["index"] <= 19 or
        20 <= idx <= 24 and 20 <= x["index"] <= 24 or
        25 <= idx <= 29 and 25 <= x["index"] <= 29 or
        30 <= idx <= 34 and 30 <= x["index"] <= 34 or
        35 <= idx <= 39 and 35 <= x["index"] <= 39 or
        40 <= idx <= 45 and 40 <= x["index"] <= 45 or
        46 <= idx <= 50 and 46 <= x["index"] <= 50 or
        51 <= idx <= 55 and 51 <= x["index"] <= 55 or
        56 <= idx <= 60 and 56 <= x["index"] <= 60
    )]) + 1

    clean_lectures.append({
        "id": f"LEC-{idx:02d}",
        "index": idx,
        "week_num": w_num,
        "week_title": week_names[w_num],
        "lecture_num": lec_num,
        "title": title_overrides.get(idx, c["lecture_title"]),
        "instructor": c["instructor"],
        "start_page": c["start_page"],
        "end_page": c["end_page"],
        "page_count": c["page_count"]
    })

with open("final_lectures.json", "w", encoding="utf-8") as f:
    json.dump(clean_lectures, f, indent=2, ensure_ascii=False)

print("Saved final_lectures.json with 60 cleanly structured lectures.")
