import sqlite3
import json
import os
import re

# -------------------------------------------------------------
# 1. Clean Stems Function for 1,560 MCQs
# -------------------------------------------------------------
def clean_question_stem(q):
    # Verb + on/in Slides? X-Y
    verbs = ['cited', 'listed', 'identified', 'discussed', 'presented', 'shown', 'outlined', 'defined', 'described', 'illustrated', 'diagrammed', 'noted', 'detailed', 'categorized']
    for v in verbs:
        q = re.sub(rf'(?i)\b{v}\s+(?:on|in)\s+(?:Slides?|Pages?)\s*[\d\s,-–and&]+\b', v, q)
        q = re.sub(rf'(?i)\bas\s+{v}\s+(?:on|in)\s+(?:Slides?|Pages?)\s*[\d\s,-–and&]+\b', f'as {v}', q)

    q = re.sub(r'(?i)\bAccording to the course slides on ([^,]+),\s*', r'In \1, ', q)
    q = re.sub(r'(?i)\bAccording to (?:the course )?(?:Slides?|Pages?)\s*[\d\s,-–and&]+,\s*', 'In Management Information Systems, ', q)
    q = re.sub(r'(?i)\bAccording to (?:the course )?(?:Slides?|Pages?)\b', 'in MIS principles', q)

    q = re.sub(r'(?i)^On (?:Slides?|Pages?)\s*[\d\s,-–and&]+,\s*', 'In business information systems, ', q)
    q = re.sub(r'\s*\((?:Slides?|Pages?|slides?|pages?)\s*[\d\s,-–and&]+\)', '', q)

    q = re.sub(r'(?i)\s+as\s+(?:outlined|detailed|discussed|presented|described|shown)\s+(?:on|in)\s+(?:Slides?|Pages?)\s*[\d\s,-–and&]+', '', q)
    q = re.sub(r'(?i)\s+(?:outlined|detailed|discussed|presented|described|shown)\s+(?:on|in)\s+(?:Slides?|Pages?)\s*[\d\s,-–and&]+', '', q)

    q = re.sub(r'(?i)^In (?:Slides?|Pages?)\s*[\d\s,-–and&]+,\s*', 'In Management Information Systems, ', q)
    q = re.sub(r'(?i)\bIn (?:Slides?|Pages?)\s*[\d\s,-–and&]+,\s*', '', q)

    q = re.sub(r'(?i)\s+on (?:Slides?|Pages?)\s*[\d\s,-–and&]+', '', q)
    q = re.sub(r'(?i)\s+in (?:Slides?|Pages?)\s*[\d\s,-–and&]+', '', q)
    q = re.sub(r'(?i)\s+from (?:Slides?|Pages?)\s*[\d\s,-–and&]+', '', q)

    q = re.sub(r'(?i)\s*(?:slides?|pages?)\s*[\d\s,-–and&]+\?', '?', q)
    q = re.sub(r'(?i)\s*(?:slides?|pages?)\s*\d+\b', '', q)

    q = re.sub(r'^[,\s]+', '', q)
    q = re.sub(r'\s+([?,.])', r'\1', q)
    q = re.sub(r'\s{2,}', ' ', q).strip()
    if q and q[0].islower():
        q = q[0].upper() + q[1:]
    return q

# -------------------------------------------------------------
# 2. Official Assignment Questions & Solutions Data (120 MCQs)
# -------------------------------------------------------------
ASSIGNMENTS_DATA = [
    # WEEK 1 (Pages 1-3)
    {
        "week": 1,
        "questions": [
            {
                "num": 1,
                "text": "What is the primary goal of MIS?",
                "options": {
                    "A": "Increase hardware sales",
                    "B": "Generate raw data",
                    "C": "Transform data into useful information for decision-making",
                    "D": "Replace managers"
                },
                "ans": "C",
                "pdf_page": 1,
                "topic": "Primary Goals of MIS",
                "solution": "The foundational definition of a Management Information System (MIS) is to collect, process, store, and transform raw facts (data) into meaningful, structured information that supports organizational decision-making, operational coordination, and managerial control."
            },
            {
                "num": 2,
                "text": "Which of the following represents the correct hierarchy?",
                "options": {
                    "A": "Wisdom → Knowledge → Information → Data",
                    "B": "Data → Information → Knowledge → Wisdom",
                    "C": "Information → Data → Wisdom → Knowledge",
                    "D": "Knowledge → Data → Information → Wisdom"
                },
                "ans": "B",
                "pdf_page": 1,
                "topic": "DIKW Pyramid Hierarchy",
                "solution": "The standard DIKW hierarchy progresses upwards from raw data (unstructured facts) → information (contextualized and structured data) → knowledge (synthesized information applied to solve problems) → wisdom (the evaluated understanding and judgment of when and how to apply knowledge)."
            },
            {
                "num": 3,
                "text": "Data can best be described as:",
                "options": {
                    "A": "Processed facts",
                    "B": "Meaningful insights",
                    "C": "Raw facts and figures",
                    "D": "Strategic decisions"
                },
                "ans": "C",
                "pdf_page": 1,
                "topic": "Definition of Data",
                "solution": "In information systems, data is explicitly defined as streams of raw facts and figures representing events occurring in organizations or the physical environment before they have been organized and arranged into a form that people can understand and use."
            },
            {
                "num": 4,
                "text": "Information is:",
                "options": {
                    "A": "Unprocessed data",
                    "B": "Data arranged in a meaningful form",
                    "C": "A collection of hardware devices",
                    "D": "Organizational culture"
                },
                "ans": "B",
                "pdf_page": 2,
                "topic": "Definition of Information",
                "solution": "Information represents data that has been shaped into a meaningful and useful context for human beings, allowing managers to interpret patterns, make informed decisions, and coordinate business actions."
            },
            {
                "num": 5,
                "text": "Which activity captures raw data in an information system?",
                "options": {
                    "A": "Processing",
                    "B": "Feedback",
                    "C": "Input",
                    "D": "Output"
                },
                "ans": "C",
                "pdf_page": 2,
                "topic": "Information System Activities (Input)",
                "solution": "Input is the activity of capturing or collecting raw data from within the organization or from its external environment for introduction into an information system."
            },
            {
                "num": 6,
                "text": "Which activity converts raw data into meaningful information?",
                "options": {
                    "A": "Feedback",
                    "B": "Processing",
                    "C": "Input",
                    "D": "Distribution"
                },
                "ans": "B",
                "pdf_page": 2,
                "topic": "Information System Activities (Processing)",
                "solution": "Processing converts raw input into meaningful information through calculations, comparisons, sorting, summarizing, and data manipulation."
            },
            {
                "num": 7,
                "text": "The output of an information system is primarily used for:",
                "options": {
                    "A": "Data collection",
                    "B": "Data storage",
                    "C": "Decision-making and actions",
                    "D": "Hardware maintenance"
                },
                "ans": "C",
                "pdf_page": 2,
                "topic": "Information System Activities (Output)",
                "solution": "Output transfers the processed information to the people who will use it or to the activities for which it will be used, primarily for managerial decision-making and operational execution."
            },
            {
                "num": 8,
                "text": "Feedback in an information system is used to:",
                "options": {
                    "A": "Increase storage capacity",
                    "B": "Correct or evaluate inputs",
                    "C": "Replace processing",
                    "D": "Eliminate outputs"
                },
                "ans": "B",
                "pdf_page": 2,
                "topic": "Information System Feedback Mechanism",
                "solution": "Feedback is output that is returned to appropriate members of the organization to help them evaluate or correct the input stage, ensuring system accuracy and adaptive operational control."
            },
            {
                "num": 9,
                "text": "Computers and software are considered:",
                "options": {
                    "A": "Complete information systems",
                    "B": "Organizational assets",
                    "C": "Technical foundations of information systems",
                    "D": "Decision makers"
                },
                "ans": "C",
                "pdf_page": 3,
                "topic": "IS Dimensions & Technical Foundation",
                "solution": "Computers and software constitute information technology (IT), which provides the technical foundation, tools, and infrastructure through which an organization builds its broader Information System (IS)."
            },
            {
                "num": 10,
                "text": "Which technology trend is highlighted as transforming business?",
                "options": {
                    "A": "Typewriters",
                    "B": "Mobile digital platforms",
                    "C": "Telegraph systems",
                    "D": "Mechanical calculators"
                },
                "ans": "B",
                "pdf_page": 3,
                "topic": "Emerging Information Technology Trends",
                "solution": "Mobile digital platforms, cloud computing, and big data analytics are the major contemporary technology trends transforming modern digital firms and business workflows."
            }
        ]
    },

    # WEEK 2 (Pages 4-6)
    {
        "week": 2,
        "questions": [
            {
                "num": 1,
                "text": "What is the smallest unit of data a computer can handle?",
                "options": {
                    "A": "Byte",
                    "B": "Field",
                    "C": "Bit",
                    "D": "Record"
                },
                "ans": "C",
                "pdf_page": 4,
                "topic": "Data Hierarchy Fundamentals",
                "solution": "A bit (binary digit) represents the smallest unit of data in computing, capable of storing a binary state of either 0 or 1. Eight bits group together to form a byte."
            },
            {
                "num": 2,
                "text": "A collection of related files is known as:",
                "options": {
                    "A": "Record",
                    "B": "Field",
                    "C": "Database",
                    "D": "Byte"
                },
                "ans": "C",
                "pdf_page": 4,
                "topic": "Data Hierarchy & Database Definition",
                "solution": "In the data hierarchy, bits form bytes (characters), bytes form fields, fields form records, records form files (tables), and a group of related files forms a database."
            },
            {
                "num": 3,
                "text": "An entity can be best described as:",
                "options": {
                    "A": "A software package",
                    "B": "A person, place, or thing about which data is stored",
                    "C": "A collection of records",
                    "D": "A database query"
                },
                "ans": "B",
                "pdf_page": 4,
                "topic": "Entity-Relationship Concepts",
                "solution": "An entity is any person, place, thing, or event in the real world about which an organization maintains stored information (e.g., CUSTOMER, PRODUCT, ORDER)."
            },
            {
                "num": 4,
                "text": "Which of the following is an attribute of a STUDENT entity?",
                "options": {
                    "A": "Database",
                    "B": "Grade",
                    "C": "Folder",
                    "D": "File"
                },
                "ans": "B",
                "pdf_page": 4,
                "topic": "Entity Attributes",
                "solution": "Attributes are specific characteristics or properties describing an entity. For a STUDENT entity, Grade, Student_ID, Name, and Major are valid attributes."
            },
            {
                "num": 5,
                "text": "Data redundancy refers to:",
                "options": {
                    "A": "Missing data",
                    "B": "Duplicate data stored in multiple files",
                    "C": "Incorrect data entry",
                    "D": "Unauthorized access"
                },
                "ans": "B",
                "pdf_page": 5,
                "topic": "Traditional File Environment Problems",
                "solution": "Data redundancy is the presence of duplicate data in multiple data files, so that the same data values are stored in more than one place, wasting storage and creating inconsistency."
            },
            {
                "num": 6,
                "text": "Data inconsistency occurs when:",
                "options": {
                    "A": "Data is encrypted",
                    "B": "Data is stored in a warehouse",
                    "C": "Same attribute has different values",
                    "D": "Data is normalized"
                },
                "ans": "C",
                "pdf_page": 5,
                "topic": "Data Inconsistency",
                "solution": "Data inconsistency exists when different copies of the same data do not agree with each other—such as when a customer address is updated in one department system but remains outdated in another."
            },
            {
                "num": 7,
                "text": "A primary key is used for:",
                "options": {
                    "A": "Data backup",
                    "B": "Data compression",
                    "C": "Unique identification of records",
                    "D": "Data mining"
                },
                "ans": "C",
                "pdf_page": 5,
                "topic": "Relational Database Keys",
                "solution": "A primary key is a field (or column) in a relational table that uniquely identifies each record (row) so that no two rows can share the exact same primary key value."
            },
            {
                "num": 8,
                "text": "A DBMS acts as:",
                "options": {
                    "A": "A spreadsheet tool",
                    "B": "An interface between applications and databases",
                    "C": "A programming language",
                    "D": "A web browser"
                },
                "ans": "B",
                "pdf_page": 5,
                "topic": "Role of Database Management Systems",
                "solution": "A Database Management System (DBMS) is software that acts as an interface between application programs and the physical data files, relieving programmers from having to understand physical data storage layouts."
            },
            {
                "num": 9,
                "text": "One major advantage of DBMS is:",
                "options": {
                    "A": "Increased redundancy",
                    "B": "Reduces inconsistency",
                    "C": "Reduced storage capacity",
                    "D": "Decentralized security"
                },
                "ans": "B",
                "pdf_page": 5,
                "topic": "Benefits of Relational DBMS",
                "solution": "A DBMS centralizes data management, minimizes data redundancy, eliminates data inconsistency, and enforces unified access security and integrity constraints across the organization."
            },
            {
                "num": 10,
                "text": "Which is a major BI tool?",
                "options": {
                    "A": "OLAP",
                    "B": "Compiler",
                    "C": "Antivirus",
                    "D": "Browser"
                },
                "ans": "A",
                "pdf_page": 6,
                "topic": "Business Intelligence (BI) Tools",
                "solution": "Online Analytical Processing (OLAP) is a cornerstone Business Intelligence capability that enables multidimensional analysis of consolidated corporate data across time, product, and regional hierarchies."
            }
        ]
    },

    # WEEK 3 (Pages 7-9)
    {
        "week": 3,
        "questions": [
            {
                "num": 1,
                "text": "SAP stands for:",
                "options": {
                    "A": "Systems Applications & Products in Data Processing",
                    "B": "Standard Applications Processing",
                    "C": "Systems and Products Platform",
                    "D": "Software Applications Processing"
                },
                "ans": "A",
                "pdf_page": 7,
                "topic": "ERP Enterprise Software (SAP)",
                "solution": "SAP is the global standard in ERP and stands for Systems, Applications, and Products in Data Processing (originally Systeme, Anwendungen und Produkte in der Datenverarbeitung)."
            },
            {
                "num": 2,
                "text": "SAP R/3 follows:",
                "options": {
                    "A": "Two-tier architecture",
                    "B": "Four-tier architecture",
                    "C": "Three-tier architecture",
                    "D": "Single-tier architecture"
                },
                "ans": "C",
                "pdf_page": 7,
                "topic": "SAP R/3 System Architecture",
                "solution": "The '3' in SAP R/3 explicitly denotes its client/server 3-tier architecture, cleanly separating the Database Layer, Application Layer, and Presentation (GUI) Layer."
            },
            {
                "num": 3,
                "text": "In SAP R/3, GUI components belong to:",
                "options": {
                    "A": "Database layer",
                    "B": "Application layer",
                    "C": "Presentation layer",
                    "D": "Middleware layer"
                },
                "ans": "C",
                "pdf_page": 7,
                "topic": "Three-Tier Client/Server Architecture",
                "solution": "The Graphical User Interface (SAP GUI) runs at the Presentation Layer on client PCs or web browsers to display data and capture user input."
            },
            {
                "num": 4,
                "text": "A key business benefit expected from ERP is:",
                "options": {
                    "A": "Increased inventory levels",
                    "B": "Integrated supply chain management",
                    "C": "Increased manual effort",
                    "D": "More isolated systems"
                },
                "ans": "B",
                "pdf_page": 7,
                "topic": "Business Value of ERP",
                "solution": "ERP integrates disparate business functions into a single unified software system and central database, enabling seamless end-to-end supply chain coordination and rapid cross-functional data sharing."
            },
            {
                "num": 5,
                "text": "ERP helps reduce:",
                "options": {
                    "A": "Order-to-cash cycle time",
                    "B": "Data availability",
                    "C": "Productivity",
                    "D": "Automation"
                },
                "ans": "A",
                "pdf_page": 8,
                "topic": "ERP Operational Efficiencies",
                "solution": "By eliminating departmental silos and automating inter-departmental handoffs, ERP dramatically accelerates the 'order-to-cash' cycle—the total time taken from receiving a customer order to collecting payment."
            },
            {
                "num": 6,
                "text": "ERP facilitates:",
                "options": {
                    "A": "Business Process Reengineering (BPR)",
                    "B": "Data duplication",
                    "C": "Information silos",
                    "D": "Stand-alone processing"
                },
                "ans": "A",
                "pdf_page": 8,
                "topic": "ERP and Business Process Reengineering",
                "solution": "ERP implementations require organizations to examine and often radically redesign their operational workflows to align with standardized best-practice industry processes (Business Process Reengineering - BPR)."
            },
            {
                "num": 7,
                "text": "ERP affects:",
                "options": {
                    "A": "Business processes",
                    "B": "Company culture",
                    "C": "Employee skills",
                    "D": "All of the above"
                },
                "ans": "D",
                "pdf_page": 8,
                "topic": "Organizational Impact of ERP",
                "solution": "ERP adoption is not merely a software upgrade; it is an organizational transformation that fundamentally impacts business processes, organizational culture, job roles, and employee technological competencies."
            },
            {
                "num": 8,
                "text": "ERP can reduce costs through:",
                "options": {
                    "A": "Better supplier management",
                    "B": "Increased redundancy",
                    "C": "More manual work",
                    "D": "Separate purchasing systems"
                },
                "ans": "A",
                "pdf_page": 8,
                "topic": "ERP Cost Reduction Mechanisms",
                "solution": "ERP provides company-wide visibility into purchasing, allowing enterprises to aggregate orders, negotiate volume discounts, and optimize supplier contracts and vendor performance."
            },
            {
                "num": 9,
                "text": "A common reason for ERP project risk is:",
                "options": {
                    "A": "Strong top management support",
                    "B": "Inexperienced core team",
                    "C": "Stable requirements",
                    "D": "High computer literacy"
                },
                "ans": "B",
                "pdf_page": 8,
                "topic": "ERP Implementation Risks",
                "solution": "ERP implementation failures typically stem from inexperienced project management teams, lack of user training, employee resistance to change, and inadequate executive championship."
            },
            {
                "num": 10,
                "text": "A limitation of traditional MRP was:",
                "options": {
                    "A": "Lack of planning capability",
                    "B": "Ignoring available capacity during planning",
                    "C": "Too much HR integration",
                    "D": "Real-time collaboration"
                },
                "ans": "B",
                "pdf_page": 9,
                "topic": "Evolution from MRP to MRP II and ERP",
                "solution": "Traditional Material Requirements Planning (MRP I) operated on infinite capacity assumptions, generating schedules based on inventory requirements while completely ignoring whether machine and labor capacity actually existed."
            }
        ]
    },

    # WEEK 4 (Pages 10-12)
    {
        "week": 4,
        "questions": [
            {
                "num": 1,
                "text": "SCM involves which two major flows?",
                "options": {
                    "A": "Product and profit flow",
                    "B": "Material flow and information flow",
                    "C": "Cash flow and tax flow",
                    "D": "Labor flow and energy flow"
                },
                "ans": "B",
                "pdf_page": 10,
                "topic": "Supply Chain Management Flows",
                "solution": "Supply Chain Management coordinates two fundamental streams: the physical flow of materials/goods from suppliers to consumers, and the bidirectional flow of information (demands, orders, shipments, and inventory states)."
            },
            {
                "num": 2,
                "text": "A supply chain is best described as a:",
                "options": {
                    "A": "Single manufacturing unit",
                    "B": "Distribution warehouse",
                    "C": "Network of resources, organizations, technologies, and processes",
                    "D": "Marketing department"
                },
                "ans": "C",
                "pdf_page": 10,
                "topic": "Supply Chain Definition",
                "solution": "A supply chain is a network of organizations and business processes for procuring materials, transforming raw materials into intermediate and finished products, and distributing the finished products to customers."
            },
            {
                "num": 3,
                "text": "One method of reducing the bullwhip effect is to:",
                "options": {
                    "A": "Increase batch sizes",
                    "B": "Improve communication across the supply chain",
                    "C": "Reduce information sharing",
                    "D": "Increase shortages"
                },
                "ans": "B",
                "pdf_page": 10,
                "topic": "Bullwhip Effect Mitigation",
                "solution": "The bullwhip effect—where demand distortion magnifies upstream—is mitigated by sharing real-time point-of-sale (POS) data, reducing batch sizes, and maintaining transparent collaborative communication across all tiers."
            },
            {
                "num": 4,
                "text": "Demand-driven supply chains use a:",
                "options": {
                    "A": "Push system",
                    "B": "Pull system",
                    "C": "Manual system",
                    "D": "Forecast-only system"
                },
                "ans": "B",
                "pdf_page": 10,
                "topic": "Push vs. Pull Supply Chain Models",
                "solution": "In a pull-based (demand-driven) model, actual customer orders trigger events in the supply chain. Materials and products are only produced and moved when dictated by real end-consumer consumption."
            },
            {
                "num": 5,
                "text": "In a Just-in-Time (JIT) strategy, components arrive:",
                "options": {
                    "A": "Months before production",
                    "B": "After product delivery",
                    "C": "As they are needed",
                    "D": "At fixed yearly intervals"
                },
                "ans": "C",
                "pdf_page": 11,
                "topic": "Just-in-Time (JIT) Manufacturing",
                "solution": "A Just-in-Time strategy coordinates supplier deliveries so that raw materials and components arrive at the factory floor precisely at the moment they are needed for production, minimizing holding costs."
            },
            {
                "num": 6,
                "text": "Which supply chain consists of suppliers and suppliers' suppliers?",
                "options": {
                    "A": "Internal supply chain",
                    "B": "Downstream supply chain",
                    "C": "Upstream supply chain",
                    "D": "Retail supply chain"
                },
                "ans": "C",
                "pdf_page": 11,
                "topic": "Upstream Supply Chain Structure",
                "solution": "The upstream portion of the supply chain includes a company's suppliers, the suppliers' suppliers (Tier 2, Tier 3), and the processes for managing relationships with them."
            },
            {
                "num": 7,
                "text": "The downstream supply chain focuses on:",
                "options": {
                    "A": "Raw material suppliers",
                    "B": "Internal warehouses",
                    "C": "Product delivery to customers",
                    "D": "Employee management"
                },
                "ans": "C",
                "pdf_page": 11,
                "topic": "Downstream Supply Chain Structure",
                "solution": "The downstream portion of the supply chain consists of the organizations and processes for distributing and delivering finished goods to the final customers."
            },
            {
                "num": 8,
                "text": "Internal supply chain activities occur:",
                "options": {
                    "A": "Between countries",
                    "B": "Inside the factory",
                    "C": "Only with customers",
                    "D": "Only with suppliers"
                },
                "ans": "B",
                "pdf_page": 11,
                "topic": "Internal Supply Chain Processes",
                "solution": "The internal supply chain encompasses the manufacturing, transformation, assembly, and packaging processes that take place inside the enterprise's own facilities."
            },
            {
                "num": 9,
                "text": "The bullwhip effect occurs when:",
                "options": {
                    "A": "Inventory is eliminated",
                    "B": "Demand information gets distorted along the supply chain",
                    "C": "Production exceeds quality standards",
                    "D": "Warehouses are automated"
                },
                "ans": "B",
                "pdf_page": 11,
                "topic": "Bullwhip Effect Mechanism",
                "solution": "The bullwhip effect occurs when small fluctuations in retail customer demand become progressively distorted and magnified as information travels back up the supply chain from retailer to distributor to manufacturer."
            },
            {
                "num": 10,
                "text": "A push-based model is also known as:",
                "options": {
                    "A": "Build-to-order",
                    "B": "Build-to-stock",
                    "C": "Demand-driven",
                    "D": "Pull-based"
                },
                "ans": "B",
                "pdf_page": 12,
                "topic": "Push-Based Production Models",
                "solution": "In a push-based model (build-to-stock), production schedules are based on forecasts or best guesses of demand for products, and products are 'pushed' to customers."
            }
        ]
    },

    # WEEK 5 (Pages 13-15)
    {
        "week": 5,
        "questions": [
            {
                "num": 1,
                "text": "A company manufactures customized industrial machinery only after receiving confirmed customer orders. This production strategy is best classified as:",
                "options": {
                    "A": "Make-to-stock",
                    "B": "Continuous production",
                    "C": "Make-to-order",
                    "D": "Batch processing"
                },
                "ans": "C",
                "pdf_page": 13,
                "topic": "Make-to-Order Manufacturing Strategy",
                "solution": "Make-to-Order (MTO) is a production approach where manufacturing begins only after an actual customer order is received, common for customized, low-volume, high-value goods."
            },
            {
                "num": 2,
                "text": "In a manufacturing information system, which document formally authorizes the start of production?",
                "options": {
                    "A": "Goods receipt note",
                    "B": "Production order",
                    "C": "Sales quotation",
                    "D": "Purchase requisition"
                },
                "ans": "B",
                "pdf_page": 13,
                "topic": "Manufacturing Execution & Work Orders",
                "solution": "A Production Order (or Work Order) is the formal document generated by the production planning system that authorizes the shop floor to produce a specified quantity of goods by a specified date."
            },
            {
                "num": 3,
                "text": "Which of the following would be considered a tactical information requirement for manufacturing management?",
                "options": {
                    "A": "Long-term product design decisions",
                    "B": "Factory location planning",
                    "C": "Quality control measures",
                    "D": "Corporate acquisition strategy"
                },
                "ans": "C",
                "pdf_page": 13,
                "topic": "Managerial Information Hierarchy (Tactical)",
                "solution": "Tactical decisions deal with medium-term resource allocation, performance monitoring, and quality control metrics, whereas factory location and corporate acquisitions are strategic."
            },
            {
                "num": 4,
                "text": "A production manager wants to identify the optimal product mix under limited machine capacity. This decision falls under:",
                "options": {
                    "A": "Strategic information",
                    "B": "Tactical information",
                    "C": "Operational information",
                    "D": "Transaction processing"
                },
                "ans": "B",
                "pdf_page": 14,
                "topic": "Tactical Capacity Optimization",
                "solution": "Determining product mix and allocating constrained machine capacity across quarters is a classic tactical management decision requiring optimization models and aggregate planning data."
            },
            {
                "num": 5,
                "text": "Which statement best explains the difference between independent and dependent demand?",
                "options": {
                    "A": "Independent demand is derived from BOM requirements.",
                    "B": "Dependent demand originates directly from customer demand.",
                    "C": "Independent demand is determined by market demand, while dependent demand is derived from it.",
                    "D": "Both are determined by suppliers."
                },
                "ans": "C",
                "pdf_page": 14,
                "topic": "Independent vs. Dependent Demand in MRP",
                "solution": "Independent demand refers to finished goods whose demand is determined directly by external market forces, whereas dependent demand refers to sub-assemblies and raw parts derived directly from the Bill of Materials."
            },
            {
                "num": 6,
                "text": "The Bill of Materials (BOM) primarily serves as:",
                "options": {
                    "A": "A financial statement",
                    "B": "A hierarchical listing of components needed to manufacture a product",
                    "C": "A quality inspection report",
                    "D": "A vendor evaluation document"
                },
                "ans": "B",
                "pdf_page": 14,
                "topic": "Bill of Materials (BOM) Structure",
                "solution": "The Bill of Materials (BOM) is a master recipe and hierarchical tree listing every subassembly, component, and raw material required to manufacture one unit of a finished product."
            },
            {
                "num": 7,
                "text": "Which MRP input specifies when finished products must be completed?",
                "options": {
                    "A": "Inventory records",
                    "B": "Capacity plan",
                    "C": "Master Production Schedule",
                    "D": "Routing sheet"
                },
                "ans": "C",
                "pdf_page": 14,
                "topic": "Master Production Schedule (MPS)",
                "solution": "The Master Production Schedule (MPS) states what finished products are to be manufactured, in what quantities, and by what exact dates."
            },
            {
                "num": 8,
                "text": "Capacity Requirement Planning (CRP) is mainly concerned with:",
                "options": {
                    "A": "Forecasting demand",
                    "B": "Determining whether sufficient production capacity exists",
                    "C": "Designing new products",
                    "D": "Monitoring customer satisfaction"
                },
                "ans": "B",
                "pdf_page": 15,
                "topic": "Capacity Requirement Planning (CRP)",
                "solution": "Capacity Requirement Planning (CRP) checks the planned orders from MRP against the machine work centers and labor hours available to verify feasibility."
            },
            {
                "num": 9,
                "text": "Which technology allows engineers to visualize and test products before physical prototypes are built?",
                "options": {
                    "A": "ERP",
                    "B": "SPC",
                    "C": "CAD",
                    "D": "CRM"
                },
                "ans": "C",
                "pdf_page": 15,
                "topic": "Computer-Aided Design (CAD)",
                "solution": "Computer-Aided Design (CAD) automates the creation, revision, and 3D simulation of designs using sophisticated graphics software prior to committing to tooling and fabrication."
            },
            {
                "num": 10,
                "text": "A major advantage of additive manufacturing over traditional manufacturing is:",
                "options": {
                    "A": "Elimination of all design costs",
                    "B": "Rapid prototyping with minimal tooling",
                    "C": "Reduced need for digital designs",
                    "D": "Lower computing requirements"
                },
                "ans": "B",
                "pdf_page": 15,
                "topic": "Additive Manufacturing (3D Printing)",
                "solution": "Additive manufacturing (3D printing) builds parts layer-by-layer directly from digital 3D models, enabling rapid prototyping and customized geometry with minimal specialized tooling."
            }
        ]
    },

    # WEEK 6 (Pages 16-18)
    {
        "week": 6,
        "questions": [
            {
                "num": 1,
                "text": "The primary objective of a Marketing Information System (MKIS) is to:",
                "options": {
                    "A": "Automate payroll processing",
                    "B": "Support marketing decision-making through relevant information",
                    "C": "Manage production schedules",
                    "D": "Monitor employee attendance"
                },
                "ans": "B",
                "pdf_page": 16,
                "topic": "Marketing Information Systems (MKIS)",
                "solution": "A Marketing Information System (MKIS) gathers, analyzes, and distributes timely, accurate information to marketing managers to improve pricing, promotion, product development, and distribution decisions."
            },
            {
                "num": 2,
                "text": "In the marketing research process, data collection should occur:",
                "options": {
                    "A": "Before defining the problem",
                    "B": "After implementing recommendations",
                    "C": "After defining objectives and research questions",
                    "D": "Before identifying information needs"
                },
                "ans": "C",
                "pdf_page": 16,
                "topic": "Marketing Research Process",
                "solution": "Methodologically, data collection can only proceed effectively after the business problem, research scope, specific objectives, and hypothesis questions have been formulated."
            },
            {
                "num": 3,
                "text": "Which subsystem continuously scans the external environment for information on competitors and market trends?",
                "options": {
                    "A": "Internal Reports Subsystem",
                    "B": "Marketing Intelligence Subsystem",
                    "C": "Pricing Subsystem",
                    "D": "Sales Forecasting Subsystem"
                },
                "ans": "B",
                "pdf_page": 16,
                "topic": "Marketing Intelligence Subsystems",
                "solution": "The Marketing Intelligence subsystem is the set of procedures and sources that managers use to obtain everyday information about pertinent developments in the external marketing environment and competitors."
            },
            {
                "num": 4,
                "text": "A company uses customer demographics, purchasing history, and psychographic data to identify target segments. This information comes primarily from:",
                "options": {
                    "A": "Customer databases",
                    "B": "Payroll records",
                    "C": "SPC systems",
                    "D": "Capacity planning systems"
                },
                "ans": "A",
                "pdf_page": 17,
                "topic": "Customer Profiling & Databases",
                "solution": "Consolidated customer databases (part of CRM and marketing systems) store transaction records, demographic profiles, and interaction channels used for market segmentation."
            },
            {
                "num": 5,
                "text": "Which forecasting method relies most heavily on historical sales patterns?",
                "options": {
                    "A": "Delphi technique",
                    "B": "Scenario planning",
                    "C": "Time-series analysis",
                    "D": "Expert panels"
                },
                "ans": "C",
                "pdf_page": 17,
                "topic": "Sales Forecasting Methods",
                "solution": "Time-series analysis relies on statistical models that analyze past chronological data points to isolate trends, seasonal cycles, and recurring patterns to project future sales."
            },
            {
                "num": 6,
                "text": "The greatest advantage of Sales Force Automation is:",
                "options": {
                    "A": "Eliminating customer interactions",
                    "B": "Instant access to organizational information during selling activities",
                    "C": "Replacing marketing research",
                    "D": "Reducing product quality costs"
                },
                "ans": "B",
                "pdf_page": 17,
                "topic": "Sales Force Automation (SFA)",
                "solution": "Sales Force Automation equips field sales reps with mobile devices that give real-time access to corporate inventories, pricing discounts, customer credit terms, and order submission tools."
            },
            {
                "num": 7,
                "text": "Before a sales order is confirmed, organizations commonly perform:",
                "options": {
                    "A": "Employee screening",
                    "B": "Credit verification",
                    "C": "Vendor rating",
                    "D": "Capacity auditing"
                },
                "ans": "B",
                "pdf_page": 17,
                "topic": "Order Management & Credit Check",
                "solution": "In order-to-cash workflows, the system automatically checks the customer's credit limit and payment history before releasing a sales order for warehouse picking."
            },
            {
                "num": 8,
                "text": "Which activity immediately follows picking and packing in the sales distribution process?",
                "options": {
                    "A": "Recruitment",
                    "B": "Payroll approval",
                    "C": "Transportation and shipment arrangement",
                    "D": "Vendor evaluation"
                },
                "ans": "C",
                "pdf_page": 17,
                "topic": "Order Fulfillment Process",
                "solution": "Once items are picked from warehouse shelves and packed into shipping cartons, logistics schedules carrier transportation, issues the bill of lading, and initiates shipping."
            },
            {
                "num": 9,
                "text": "The primary purpose of Accounts Receivable is to:",
                "options": {
                    "A": "Manage supplier payments",
                    "B": "Track money owed by customers",
                    "C": "Maintain payroll records",
                    "D": "Monitor inventory"
                },
                "ans": "B",
                "pdf_page": 18,
                "topic": "Financial Information Systems (AR)",
                "solution": "Accounts Receivable (AR) records and manages debts owed to the enterprise by customers who have purchased goods or services on credit."
            },
            {
                "num": 10,
                "text": "A customer returns damaged goods after invoicing. Which accounting document is most likely generated?",
                "options": {
                    "A": "Debit note",
                    "B": "Purchase requisition",
                    "C": "Inspection certificate",
                    "D": "Credit note"
                },
                "ans": "D",
                "pdf_page": 18,
                "topic": "Billing & Accounting Adjustments",
                "solution": "A Credit Note (or Credit Memo) is issued by a seller to a buyer to reduce the amount the customer owes under an invoice, commonly due to damaged, returned, or overbilled merchandise."
            }
        ]
    },

    # WEEK 7 (Pages 19-21)
    {
        "week": 7,
        "questions": [
            {
                "num": 1,
                "text": "Business strategy is a function of:",
                "options": {
                    "A": "Competition, Positioning, and Capabilities",
                    "B": "Hardware, Software, and Data",
                    "C": "Revenue, Cost, and Profit",
                    "D": "Customers, Vendors, and Employees"
                },
                "ans": "A",
                "pdf_page": 19,
                "topic": "Strategic Alignment Framework",
                "solution": "In strategic management, an enterprise's business strategy is dictated by competitive industry forces, market positioning, and internal organizational capabilities."
            },
            {
                "num": 2,
                "text": "Which model is used for organizational design?",
                "options": {
                    "A": "SWOT Matrix",
                    "B": "Business Diamond",
                    "C": "BCG Matrix",
                    "D": "Ansoff Matrix"
                },
                "ans": "B",
                "pdf_page": 19,
                "topic": "Leavitt's Business Diamond",
                "solution": "Leavitt's Business Diamond model is a foundational framework for organizational design and change management, demonstrating that altering one component requires rebalancing the others."
            },
            {
                "num": 3,
                "text": "The Business Diamond consists of:",
                "options": {
                    "A": "Finance, Marketing, HR, Operations",
                    "B": "Hardware, Software, Network, Data",
                    "C": "People, Structure, Tasks, Information Control",
                    "D": "Cost, Quality, Time, Flexibility"
                },
                "ans": "C",
                "pdf_page": 19,
                "topic": "Business Diamond Dimensions",
                "solution": "The four interrelated corners of Leavitt's Diamond are Tasks (processes), People (skills and culture), Structure (hierarchy and organization), and Information & Technology (control mechanisms)."
            },
            {
                "num": 4,
                "text": "Which is NOT an IS infrastructure component?",
                "options": {
                    "A": "Hardware",
                    "B": "Software",
                    "C": "Network",
                    "D": "Advertising"
                },
                "ans": "D",
                "pdf_page": 19,
                "topic": "IT Infrastructure Components",
                "solution": "IT infrastructure is composed of computer hardware, software, data management technology, and networking/telecommunications facilities. Advertising is a marketing communication activity, not an IS infrastructure element."
            },
            {
                "num": 5,
                "text": "Changing one corner of the IS Strategy Triangle requires:",
                "options": {
                    "A": "No action",
                    "B": "Evaluating the other two corners",
                    "C": "Hiring more staff",
                    "D": "Increasing profits"
                },
                "ans": "B",
                "pdf_page": 20,
                "topic": "Information Systems Strategy Triangle",
                "solution": "The IS Strategy Triangle dictates that Business Strategy, Organizational Strategy, and Information Strategy must remain in balance. Changing any one corner requires evaluating and adjusting the other two."
            },
            {
                "num": 6,
                "text": "Strategic Systems Analysis examines:",
                "options": {
                    "A": "Industry structure and competitive forces",
                    "B": "Employee attendance only",
                    "C": "Payroll systems only",
                    "D": "Accounting records only"
                },
                "ans": "A",
                "pdf_page": 20,
                "topic": "Strategic Systems Analysis",
                "solution": "Strategic Systems Analysis systematically evaluates competitive industry structure, Porter's Five Forces, corporate value chains, and core competencies to identify high-ROI strategic IT opportunities."
            },
            {
                "num": 7,
                "text": "Balanced Scorecard (BSC) focuses on:",
                "options": {
                    "A": "Only financial performance",
                    "B": "Four dimensions of performance",
                    "C": "Employee salaries",
                    "D": "Product prices only"
                },
                "ans": "B",
                "pdf_page": 20,
                "topic": "Balanced Scorecard Framework",
                "solution": "Developed by Kaplan and Norton, the Balanced Scorecard supplements traditional financial measures with three operational perspectives: Customer, Internal Business Processes, and Learning & Growth."
            },
            {
                "num": 8,
                "text": "Which is NOT one of the four BSC dimensions?",
                "options": {
                    "A": "Customer",
                    "B": "Financial",
                    "C": "Business Process",
                    "D": "Manufacturing Capacity"
                },
                "ans": "D",
                "pdf_page": 20,
                "topic": "Four Balanced Scorecard Perspectives",
                "solution": "The official four dimensions are Financial, Customer, Internal Business Processes, and Learning/Growth. Manufacturing Capacity is a specific operational sub-metric, not a distinct BSC perspective."
            },
            {
                "num": 9,
                "text": "KPIs in a BSC are:",
                "options": {
                    "A": "Key Performance Indicators",
                    "B": "Knowledge Processing Instructions",
                    "C": "Key Product Integrators",
                    "D": "Knowledge Performance Interfaces"
                },
                "ans": "A",
                "pdf_page": 20,
                "topic": "Key Performance Indicators (KPIs)",
                "solution": "KPIs stands for Key Performance Indicators—quantifiable metrics used by managers to evaluate an organization's progress toward achieving its strategic goals."
            },
            {
                "num": 10,
                "text": "BSC helps managers focus on:",
                "options": {
                    "A": "Strategic vision",
                    "B": "Office administration only",
                    "C": "Accounting entries only",
                    "D": "Legal compliance only"
                },
                "ans": "A",
                "pdf_page": 21,
                "topic": "Balanced Scorecard Strategic Alignment",
                "solution": "The fundamental purpose of the Balanced Scorecard is to translate an organization's overarching mission and strategic vision into concrete, actionable performance objectives."
            }
        ]
    },

    # WEEK 8 (Pages 22-24)
    {
        "week": 8,
        "questions": [
            {
                "num": 1,
                "text": "E-commerce refers to:",
                "options": {
                    "A": "Physical transactions only",
                    "B": "Digitally enabled commercial transactions involving exchange of value",
                    "C": "Internal organizational communication",
                    "D": "Manufacturing automation"
                },
                "ans": "B",
                "pdf_page": 22,
                "topic": "E-Commerce Definition",
                "solution": "E-commerce is defined formally as digitally enabled commercial transactions between and among organizations and individuals, involving the exchange of economic value across institutional boundaries."
            },
            {
                "num": 2,
                "text": "Which feature of e-commerce allows access to markets anytime and anywhere?",
                "options": {
                    "A": "Richness",
                    "B": "Interactivity",
                    "C": "Ubiquity",
                    "D": "Customization"
                },
                "ans": "C",
                "pdf_page": 22,
                "topic": "Ubiquity Dimension of E-Commerce",
                "solution": "Ubiquity means internet/web technology is available everywhere: at work, at home, and elsewhere via mobile devices anytime, creating a 'marketspace' liberated from physical location."
            },
            {
                "num": 3,
                "text": "The ability of e-commerce to reach across national boundaries is known as:",
                "options": {
                    "A": "Information density",
                    "B": "Global reach",
                    "C": "Personalization",
                    "D": "Interactivity"
                },
                "ans": "B",
                "pdf_page": 22,
                "topic": "Global Reach in Digital Markets",
                "solution": "Global reach refers to the technology's capability to traverse national boundaries seamlessly, making commerce possible across cultural and national geographic perimeters."
            },
            {
                "num": 4,
                "text": "Information density in e-commerce means information is:",
                "options": {
                    "A": "Limited and costly",
                    "B": "Plentiful, cheap, and accurate",
                    "C": "Only available to firms",
                    "D": "Difficult to access"
                },
                "ans": "B",
                "pdf_page": 22,
                "topic": "Information Density",
                "solution": "Information density is the total amount and quality of information available to all market participants. E-commerce dramatically lowers storage, communication, and processing costs while raising timeliness."
            },
            {
                "num": 5,
                "text": "Adjusting marketing messages based on a customer's clickstream behavior is called:",
                "options": {
                    "A": "Customization",
                    "B": "Segmentation",
                    "C": "Personalization",
                    "D": "Automation"
                },
                "ans": "C",
                "pdf_page": 23,
                "topic": "Personalization in E-Commerce",
                "solution": "Personalization allows merchants to target marketing messages to specific individuals by adjusting the message to a person's name, interests, clickstream history, and past purchases."
            },
            {
                "num": 6,
                "text": "Changing a delivered product based on user preferences is known as:",
                "options": {
                    "A": "Personalization",
                    "B": "Customization",
                    "C": "Standardization",
                    "D": "Diversification"
                },
                "ans": "B",
                "pdf_page": 23,
                "topic": "Customization in E-Commerce",
                "solution": "Customization involves changing the delivered product or service based on a user's explicit preferences or prior behavior."
            },
            {
                "num": 7,
                "text": "Amazon is an example of which type of e-commerce?",
                "options": {
                    "A": "B2B",
                    "B": "C2C",
                    "C": "B2C",
                    "D": "G2C"
                },
                "ans": "C",
                "pdf_page": 23,
                "topic": "Business-to-Consumer (B2C) E-Commerce",
                "solution": "Business-to-Consumer (B2C) e-commerce involves retailing products and services to individual consumer shoppers, of which Amazon is the global archetype."
            },
            {
                "num": 8,
                "text": "IndiaMART is primarily an example of:",
                "options": {
                    "A": "B2B e-commerce",
                    "B": "C2C e-commerce",
                    "C": "Social commerce",
                    "D": "Mobile commerce"
                },
                "ans": "A",
                "pdf_page": 23,
                "topic": "Business-to-Business (B2B) Marketplaces",
                "solution": "IndiaMART is an online B2B marketplace platform that connects wholesale buyers with manufacturers, distributors, and suppliers."
            },
            {
                "num": 9,
                "text": "Which of the following is a major challenge in e-commerce?",
                "options": {
                    "A": "Global reach",
                    "B": "Personalization",
                    "C": "Trust issues",
                    "D": "Richness"
                },
                "ans": "C",
                "pdf_page": 23,
                "topic": "E-Commerce Security & Trust Challenges",
                "solution": "Trust issues (transactional fraud, identity theft, credit card privacy, and vendor legitimacy) remain among the foremost behavioral barriers in online commerce."
            },
            {
                "num": 10,
                "text": "Which key element of a business model answers 'How to earn money?'",
                "options": {
                    "A": "Market strategy",
                    "B": "Competitive advantage",
                    "C": "Revenue model",
                    "D": "Market opportunity"
                },
                "ans": "C",
                "pdf_page": 24,
                "topic": "E-Commerce Revenue Models",
                "solution": "An enterprise's revenue model describes explicitly how the firm will earn revenue, generate profits, and produce a superior return on invested capital."
            }
        ]
    },

    # WEEK 9 (Pages 25-28)
    {
        "week": 9,
        "questions": [
            {
                "num": 1,
                "text": "Which of the following is not a benefit of cloud computing?",
                "options": {
                    "A": "Usage-based pricing",
                    "B": "Resource Pooling",
                    "C": "Increased Set-up Time",
                    "D": "Measured Use"
                },
                "ans": "C",
                "pdf_page": 25,
                "topic": "Cloud Computing Characteristics",
                "solution": "Cloud computing offers rapid elasticity and on-demand provisioning, which dramatically decreases (rather than increases) infrastructure setup time."
            },
            {
                "num": 2,
                "text": "Salesforce.com's CRM software is an example of which cloud service model?",
                "options": {
                    "A": "IaaS",
                    "B": "PaaS",
                    "C": "SaaS",
                    "D": "DaaD"
                },
                "ans": "C",
                "pdf_page": 25,
                "topic": "Software as a Service (SaaS)",
                "solution": "Salesforce provides an end-user application accessible entirely over web browsers without requiring customers to manage operating systems or servers, making it a classic SaaS model."
            },
            {
                "num": 3,
                "text": "FinTech Solutions Inc. is developing a new customer-facing analytics portal. To accelerate their release timeline, they decide to use a cloud-based environment where the vendor hosts the runtime, libraries, testing tools, and plugins. Which cloud service model is FinTech Solutions utilizing for this analytics portal, and who is fundamentally responsible for ensuring the availability, bandwidth, and security at the hypervisor layer?",
                "options": {
                    "A": "PaaS; The Cloud Vendor is responsible for the underlying infrastructure capacity, virtual networking, and hypervisor security.",
                    "B": "PaaS; The Client manages the physical hardware, while the Cloud Vendor manages capacity.",
                    "C": "SaaS; The Cloud Vendor manages only the application logic, while the Client manages all security and networking.",
                    "D": "SaaS; The Cloud Vendor and Client share the hypervisor layer responsibility."
                },
                "ans": "A",
                "pdf_page": 26,
                "topic": "Platform as a Service (PaaS) Shared Responsibility",
                "solution": "PaaS supplies the execution environment and development libraries. In PaaS, the cloud provider manages infrastructure, virtual networking, hypervisors, and physical hardware, while the customer manages application code and data."
            },
            {
                "num": 4,
                "text": "GlobalHealth Inc. uses its own dedicated, single-tenant servers to securely store highly sensitive patient data. To handle unpredictable spikes in public appointment bookings, the company temporarily offloads web traffic to a globally shared network. What cloud deployment model does GlobalHealth Inc. utilize?",
                "options": {
                    "A": "Public cloud",
                    "B": "Community cloud",
                    "C": "Private cloud",
                    "D": "Hybrid cloud"
                },
                "ans": "D",
                "pdf_page": 26,
                "topic": "Hybrid Cloud Architecture",
                "solution": "A hybrid cloud deployment combines internal on-premises private infrastructure (for sensitive medical records) with public cloud instances (for handling variable web traffic spikes and appointment portals)."
            },
            {
                "num": 5,
                "text": "Tools or mechanisms that can change their own state and/or the state of other devices and machines are called _______________.",
                "options": {
                    "A": "Sensors",
                    "B": "IoT",
                    "C": "Actuators",
                    "D": "Proximity Sensor"
                },
                "ans": "C",
                "pdf_page": 26,
                "topic": "IoT Actuators",
                "solution": "While sensors detect and measure physical phenomena, actuators are mechanisms that convert electronic control signals into physical actions (moving, heating, opening valves, or switching relays)."
            },
            {
                "num": 6,
                "text": "Which of the following best describes the core approach of Privacy by Design?",
                "options": {
                    "A": "Applying privacy settings as an optional add-on near the end of a project's development",
                    "B": "Proactively considering privacy objectives from the start and throughout the design and delivery",
                    "C": "Reacting to data breaches by applying immediate remedial software patches",
                    "D": "Allowing users to manually select every privacy feature from a complex menu"
                },
                "ans": "B",
                "pdf_page": 27,
                "topic": "Privacy by Design Principles",
                "solution": "Privacy by Design dictates that privacy and data protection are embedded proactively into the technological architecture and business processes from the very inception of system development."
            },
            {
                "num": 7,
                "text": "What is the primary function of a sensor in an IoT system?",
                "options": {
                    "A": "To convert an electrical signal into a physical action",
                    "B": "To capture environmental data and convert it into an electrical signal",
                    "C": "To store massive amounts of data in the cloud",
                    "D": "To provide power to the IoT device"
                },
                "ans": "B",
                "pdf_page": 27,
                "topic": "IoT Sensors",
                "solution": "Sensors detect physical inputs (temperature, vibration, pressure, light) from the physical environment and convert them into measurable electronic signals."
            },
            {
                "num": 8,
                "text": "Which of the following statements accurately describes an Outsourced Private Cloud?",
                "options": {
                    "A": "It is implemented solely within the customer's own premises.",
                    "B": "The server side is managed by a hosting company.",
                    "C": "It is designed and shared to serve the general public.",
                    "D": "The infrastructure is always owned and operated by the customer's internal IT team."
                },
                "ans": "B",
                "pdf_page": 27,
                "topic": "Outsourced Private Cloud",
                "solution": "In an outsourced private cloud, the infrastructure is dedicated exclusively to one single organization but is physically housed, managed, and maintained offsite by a third-party hosting company."
            },
            {
                "num": 9,
                "text": "A retail e-commerce giant is consolidating multiple distinct data streams from their 2026 Black Friday campaign to predict consumer churn. They aggregate Stream A (binary biometric data), Stream B (unstructured social text and emojis), and Stream C (structured SQL logs). They discover 15% missing timestamps and 20% spam bots. Which of the following best diagnoses the system's challenges by correctly applying the concepts of Variety and Veracity?",
                "options": {
                    "A": "The integration of wearable devices, social media, and transactional logs represents a Variety challenge, while timestamp gaps and spam bots represent a Veracity challenge.",
                    "B": "The data format differences between binary files, text, and JSON represent a Veracity challenge, while missing timestamps in the wearable data represent a Variety challenge.",
                    "C": "The integration of different platforms (sensors, social media, SQL) represents a Veracity challenge, while the presence of bot spam and missing intervals both strictly represent Variety issues.",
                    "D": "Both the format differences (Stream A, B, C) and the missing intervals are examples of Variety, whereas the presence of bot spam is an example of Veracity."
                },
                "ans": "A",
                "pdf_page": 28,
                "topic": "Big Data Dimensions: Variety vs. Veracity",
                "solution": "Variety encompasses different formats (binary sensor streams, text reviews, structured relational tables). Veracity refers to data trustworthiness, cleanliness, and fidelity (missing timestamps and fraudulent bot spam)."
            },
            {
                "num": 10,
                "text": "Which among the following is a cloud service provider?",
                "options": {
                    "A": "Netflix",
                    "B": "JioHotstar",
                    "C": "Reliance Digital",
                    "D": "DigitalOcean"
                },
                "ans": "D",
                "pdf_page": 28,
                "topic": "Cloud Infrastructure Providers",
                "solution": "DigitalOcean is a prominent cloud infrastructure provider offering on-demand virtual compute droplets, storage, and networking."
            }
        ]
    },

    # WEEK 10 (Pages 29-31)
    {
        "week": 10,
        "questions": [
            {
                "num": 1,
                "text": "____________ is the collective and individual experience of applying knowledge to the solution of problem; knowing when, where, and how to apply that knowledge.",
                "options": {
                    "A": "Cognition",
                    "B": "Wisdom",
                    "C": "Tacit",
                    "D": "Culture"
                },
                "ans": "B",
                "pdf_page": 29,
                "topic": "Knowledge Hierarchy (Wisdom)",
                "solution": "Wisdom is defined in MIS as the collective and individual experience of applying knowledge to solve problems, encompassing practical judgment of when, where, and how to apply insights."
            },
            {
                "num": 2,
                "text": "A retail manager uses an IT system that instantly pulls historical sales data and expert staff insights to determine the best price for a new product line. Which system is being used to practically apply organizational knowledge and add ROI to this decision?",
                "options": {
                    "A": "Transaction Processing System",
                    "B": "Office Automation System",
                    "C": "Supply Chain Management System",
                    "D": "Decision Support System (DSS)"
                },
                "ans": "D",
                "pdf_page": 29,
                "topic": "Decision Support Systems (DSS)",
                "solution": "A Decision Support System (DSS) combines analytical models, historical transaction data, and manager judgment to support semi-structured decision scenarios such as pricing optimization."
            },
            {
                "num": 3,
                "text": "Which of the following best describes a primary difference between a Neural Network and a Genetic Algorithm in organizational knowledge management?",
                "options": {
                    "A": "Genetic Algorithms are used to discover hidden patterns in data, whereas Neural Networks are used to evaluate alternative solutions.",
                    "B": "Neural Networks are used to discover patterns in data, whereas Genetic Algorithms are used to evaluate and optimize alternative solutions.",
                    "C": "Neural Networks rely on Darwinian evolution, while Genetic Algorithms rely on human nervous system models.",
                    "D": "Both act identically but process data sequentially rather than in parallel."
                },
                "ans": "B",
                "pdf_page": 29,
                "topic": "AI Techniques in Knowledge Systems",
                "solution": "Neural Networks excel at pattern recognition and classification from vast empirical datasets, whereas Genetic Algorithms excel at optimization problems by evaluating alternative candidate solutions through simulated evolutionary processes."
            },
            {
                "num": 4,
                "text": "Which scenario best illustrates a semi-structured decision type?",
                "options": {
                    "A": "Adjusting the monthly production output purely according to historical seasonal sales data.",
                    "B": "Formulating an annual corporate budget by rigidly enforcing standard inflation-adjusted formulas.",
                    "C": "Determining the most cost-effective customized delivery route for a new, irregularly shaped geographical zone.",
                    "D": "Approving a standard expense report that strictly complies with the published company travel policy."
                },
                "ans": "C",
                "pdf_page": 30,
                "topic": "Decision Characteristics: Semi-Structured Decisions",
                "solution": "Determining an optimal routing configuration across an irregular geography contains both structured mathematical constraints (mileage, transit speeds) and unstructured human judgment (road hazards, driver familiarity), making it semi-structured."
            },
            {
                "num": 5,
                "text": "Which of the following is not a phase in a decision-making process?",
                "options": {
                    "A": "Intelligence",
                    "B": "Design",
                    "C": "Choice",
                    "D": "Scope"
                },
                "ans": "D",
                "pdf_page": 30,
                "topic": "Simon's Four Stages of Decision-Making",
                "solution": "Herbert Simon's classic four stages of decision-making are Intelligence (problem identification), Design (solution development), Choice (selecting among alternatives), and Implementation. 'Scope' is not one of Simon's stages."
            },
            {
                "num": 6,
                "text": "According to the principles of Management Information Systems, which type of decisions do Executive Support Systems (ESS) primarily address?",
                "options": {
                    "A": "Routine and highly structured operational decisions",
                    "B": "Non-routine decisions requiring judgment, evaluation, and insight",
                    "C": "Strictly day-to-day tactical management decisions",
                    "D": "Pre-programmed, repetitive transaction processing"
                },
                "ans": "B",
                "pdf_page": 30,
                "topic": "Executive Support Systems (ESS)",
                "solution": "Executive Support Systems (ESS) serve senior executive management by addressing non-routine decisions requiring strategic judgment, evaluation, and holistic organizational insight."
            },
            {
                "num": 7,
                "text": "Which of the following statements best defines object-based knowledge representation for expert systems?",
                "options": {
                    "A": "Knowledge is represented as simple true/false statements without any attached data.",
                    "B": "Knowledge is represented as a network of objects, where each object contains both data and the methods that act on that data.",
                    "C": "Knowledge is strictly stored as a sequential list of procedural algorithms.",
                    "D": "Knowledge is represented purely through unstructured text files."
                },
                "ans": "B",
                "pdf_page": 30,
                "topic": "Knowledge Representation Schemes",
                "solution": "In object-oriented knowledge representation, concepts and physical entities are stored as discrete objects that encapsulate both descriptive attributes (data) and executable behaviors (methods)."
            },
            {
                "num": 8,
                "text": "A local hospital is using an AI expert system to help emergency doctors diagnose patients with severe respiratory distress. When a patient arrives, the doctor first inputs specific symptoms (e.g., sudden fever, dry cough, and shortness of breath) into the system. The inference engine immediately analyzes these available facts, checks them against thousands of nested medical rules, and progressively infers potential conditions and treatment options until it derives a set of probable diagnoses. Based on how the inference engine processes the data, which reasoning strategy is the system using?",
                "options": {
                    "A": "Backward Chaining",
                    "B": "Goal-Driven Analysis",
                    "C": "Breadth-First Deductive Reasoning",
                    "D": "Forward Chaining"
                },
                "ans": "D",
                "pdf_page": 31,
                "topic": "Inference Engines: Forward vs. Backward Chaining",
                "solution": "Forward chaining is a data-driven reasoning strategy: it begins with gathered empirical facts and symptoms, fires rules whose conditions match those facts, and proceeds forward to infer a conclusion (diagnosis)."
            },
            {
                "num": 9,
                "text": "What do the letters in the acronym MOODLE stand for?",
                "options": {
                    "A": "Modern Object-Oriented Dynamic Learning Environment",
                    "B": "Modular Object-Oriented Dynamic Learning Environment",
                    "C": "Managed Open Online Distance Learning Experience",
                    "D": "Modular Open Online Digital Learning Engine"
                },
                "ans": "B",
                "pdf_page": 31,
                "topic": "Learning Management Systems (MOODLE)",
                "solution": "MOODLE is the global open-source learning management standard and stands for Modular Object-Oriented Dynamic Learning Environment."
            },
            {
                "num": 10,
                "text": "Which type of managerial decision is routine, repetitive, and follows a predefined set of rules or standard operating procedures?",
                "options": {
                    "A": "Semi-structured",
                    "B": "Unstructured",
                    "C": "Structured",
                    "D": "Analytical"
                },
                "ans": "C",
                "pdf_page": 31,
                "topic": "Structured Decision Making",
                "solution": "Structured decisions are repetitive and routine, involving a definite, standardized procedure for handling them so that they do not have to be treated as brand new each time (e.g. inventory restocking or overtime approval)."
            }
        ]
    },

    # WEEK 11 (Pages 32-35)
    {
        "week": 11,
        "questions": [
            {
                "num": 1,
                "text": "Which of the following statements regarding the Right to Privacy is false?",
                "options": {
                    "A": "It involves the right to be left alone and free from unreasonable personal intrusions.",
                    "B": "It is an absolute right that takes total precedence over the needs of society.",
                    "C": "It must be balanced against the broader needs and interests of society.",
                    "D": "The public's right to know is often considered superior to an individual's right to privacy."
                },
                "ans": "B",
                "pdf_page": 32,
                "topic": "Ethical and Social Dimensions of Privacy",
                "solution": "In legal and ethical philosophy, privacy is not an absolute right; it must be balanced against public safety, law enforcement mandates, national security, and societal welfare."
            },
            {
                "num": 2,
                "text": "What are computer cookies, as described in web technology?",
                "options": {
                    "A": "Small text files deposited on a computer's hard drive to identify and track visits",
                    "B": "Hidden software applications that delete a user's browsing history",
                    "C": "Programs used by hackers to steal personal passwords",
                    "D": "Temporary internet cables that connect to web servers"
                },
                "ans": "A",
                "pdf_page": 32,
                "topic": "Web Privacy & Tracking Technologies",
                "solution": "Cookies are small text strings deposited on a client device's browser by web servers to record site preferences, remember shopping carts, and track user navigation."
            },
            {
                "num": 3,
                "text": "Zenith Corp implements a new Information System (IS) that tracks keystrokes, active window times, and web browsing habits. During the rollout, management announces that the system will generate random, automated performance audits, but the exact tracking schedule is kept strictly confidential. Initially, a few remote workers attempt to browse non-work-related websites during business hours. However, realising the logging software could be recording their activity at any given minute, employees began limiting their computer use strictly to corporate tasks. Which of the following best explains why Zenith Corp employees consistently conform to company policies despite the lack of a visible or constant human supervisor?",
                "options": {
                    "A": "Hawthorne Effect",
                    "B": "The Panopticon Effect",
                    "C": "Groupthink",
                    "D": "Cognitive Dissonance"
                },
                "ans": "B",
                "pdf_page": 32,
                "topic": "Surveillance & The Panopticon Effect",
                "solution": "The Panopticon effect (originally conceptualized by Jeremy Bentham and expanded by Michel Foucault) explains how subjects alter and discipline their behavior because they know they might be monitored at any moment, even if monitoring is not continuous."
            },
            {
                "num": 4,
                "text": "Which of the following best describes the primary objective and function of a Man-in-the-Middle attack?",
                "options": {
                    "A": "It overloads a target server's resources to cause a sudden disruption in legitimate user access.",
                    "B": "It secretly intercepts, reads, and potentially alters communications between a sender and a recipient without their knowledge.",
                    "C": "It tricks users into downloading and installing malicious software disguised as legitimate applications.",
                    "D": "It guesses passwords by systematically trying thousands of combinations until the correct one is found."
                },
                "ans": "B",
                "pdf_page": 33,
                "topic": "Cybersecurity Threats: MITM Attacks",
                "solution": "In a Man-in-the-Middle (MITM) attack, the perpetrator secretly intercepts and relays communications between two parties who believe they are directly communicating with each other."
            },
            {
                "num": 5,
                "text": "Which of the following cyber threats uses manipulative communication—such as bogus emails or messages—as its primary delivery method to steal an identity?",
                "options": {
                    "A": "Pharming",
                    "B": "DNS Cache Poisoning",
                    "C": "Malware Encryption",
                    "D": "Phishing"
                },
                "ans": "D",
                "pdf_page": 33,
                "topic": "Social Engineering & Phishing",
                "solution": "Phishing is a social engineering attack that involves sending deceptive emails or messages purporting to be from reputable companies to induce individuals to reveal passwords and credit card numbers."
            },
            {
                "num": 6,
                "text": "Which of the following is the full form of VPN?",
                "options": {
                    "A": "Visual Private Network",
                    "B": "Virtual Private Node",
                    "C": "Virtual Private Network",
                    "D": "Visual Private Node"
                },
                "ans": "C",
                "pdf_page": 33,
                "topic": "Network Security (VPN)",
                "solution": "A Virtual Private Network (VPN) creates a secure, encrypted tunnel over public telecommunications networks (like the internet) to allow remote users secure access to corporate intranets."
            },
            {
                "num": 7,
                "text": "A major server outage brings down the primary database for GlobalTech Solutions, instantly preventing their customer service team from accessing client records. While the IT department works on restoring the servers from the latest backup, the management team activates a backup procedure allowing agents to manually process urgent client requests using printed logs and temporary phone lines. In this scenario, which plans were demonstrated by the IT department and the management team, respectively?",
                "options": {
                    "A": "Both the IT team and management demonstrated the Disaster Recovery Plan (DRP)",
                    "B": "Both the IT team and management demonstrated the Business Continuity Plan (BCP)",
                    "C": "The IT team demonstrated the Business Continuity Plan (BCP), and management demonstrated the Disaster Recovery Plan (DRP)",
                    "D": "The IT team demonstrated the Disaster Recovery Plan (DRP), and management demonstrated the Business Continuity Plan (BCP)"
                },
                "ans": "D",
                "pdf_page": 34,
                "topic": "Disaster Recovery vs. Business Continuity Planning",
                "solution": "Disaster Recovery Planning (DRP) focuses technical efforts on restoring computing facilities, networks, and databases. Business Continuity Planning (BCP) focuses on managerial operational workarounds to keep business functions alive during an outage."
            },
            {
                "num": 8,
                "text": "Which of the following is a primary requirement for financial institutions under the Gramm-Leach-Bliley Act (GLBA) regarding customer data?",
                "options": {
                    "A": "To publicly disclose all customer account balances in a quarterly directory.",
                    "B": "To ensure the security and confidentiality of customer non-public personal information.",
                    "C": "To share customer financial data with unaffiliated third parties by default.",
                    "D": "To destroy all customer financial records after one year of inactivity."
                },
                "ans": "B",
                "pdf_page": 34,
                "topic": "Regulatory Compliance (GLBA)",
                "solution": "The Gramm-Leach-Bliley Act (GLBA) mandates that financial institutions establish comprehensive security programs to ensure the confidentiality and integrity of non-public consumer financial records."
            },
            {
                "num": 9,
                "text": "Which of the following is not considered a primary problem or objective addressed by computer forensics?",
                "options": {
                    "A": "Recovering data from computers while preserving evidential integrity",
                    "B": "Finding significant information in a large volume of electronic data",
                    "C": "Altering recovered data to better suit a specific court argument",
                    "D": "Presenting the information to a court of law"
                },
                "ans": "C",
                "pdf_page": 34,
                "topic": "Computer Forensics Integrity",
                "solution": "Computer forensics strictly requires preserving evidential chain-of-custody without tampering. Altering or fabricating data violates legal and forensic ethics."
            },
            {
                "num": 10,
                "text": "Which of the following is one of the leading Unified Threat Management (UTM) vendors?",
                "options": {
                    "A": "Fortinent",
                    "B": "McAfee",
                    "C": "Trend Micro",
                    "D": "Symantec"
                },
                "ans": "A",
                "pdf_page": 35,
                "topic": "Unified Threat Management (UTM)",
                "solution": "Fortinet (noted as Fortinent in NPTEL question transcript) is a premier global vendor specializing in enterprise Unified Threat Management appliances and next-generation firewalls."
            }
        ]
    },

    # WEEK 12 (Pages 36-39)
    {
        "week": 12,
        "questions": [
            {
                "num": 1,
                "text": "Which of the following is not a characteristic of a global organization?",
                "options": {
                    "A": "Large-scale operations",
                    "B": "A large number of middlemen",
                    "C": "Multi-Language, Mono-Cultural",
                    "D": "High risk"
                },
                "ans": "C",
                "pdf_page": 36,
                "topic": "Characteristics of Global Organizations",
                "solution": "Global organizations operate across diverse regional markets and are distinctly multi-cultural and multi-lingual. A 'mono-cultural' profile is antithetical to global enterprise reality."
            },
            {
                "num": 2,
                "text": "What is the very first step a firm must take when developing an International Information Systems Architecture?",
                "options": {
                    "A": "Designing new business procedures and reengineering",
                    "B": "Understanding the global environment and business drivers",
                    "C": "Developing the corporate global strategy",
                    "D": "Selecting the appropriate technology platform"
                },
                "ans": "B",
                "pdf_page": 36,
                "topic": "International Information Systems Architecture",
                "solution": "The first step in building a global systems architecture is to understand the external global environment: competitive business drivers, regional regulatory hurdles, and communication constraints."
            },
            {
                "num": 3,
                "text": "GlobalTech Inc. is a global electronics manufacturer. Originally, its US headquarters made all product and marketing decisions, giving overseas branches very little freedom. Recently, the company restructured so that its subsidiaries in Japan, Germany, and India operate as highly integrated yet independent units. These local branches now have the autonomy to design specific products and marketing campaigns tailored to their own cultures, while still sharing global operational efficiencies. Based on the transition described, which of the following best represents the shift in GlobalTech Inc.'s organizational strategy?",
                "options": {
                    "A": "From a Domestic Exporter to a Franchiser",
                    "B": "From a Transnational Corporation to a Multinational Corporation",
                    "C": "From a Franchiser to a Domestic Exporter",
                    "D": "From a Multinational Corporation to a Transnational Corporation"
                },
                "ans": "D",
                "pdf_page": 37,
                "topic": "Global Organizational Strategies",
                "solution": "Transnational firms optimize global operational scale while decentralizing and empowering regional business units to tailor products to local markets, representing the shift from a traditional multinational/centralized structure."
            },
            {
                "num": 4,
                "text": "An international bank's fraud detection engine continuously co-develops algorithms through real-time data sharing between teams in New York, London, and Tokyo. Each global hub simultaneously builds local patches while immediately syncing operational updates across the entire corporate infrastructure to maintain uniform security. Which systems configuration does this corporate strategy illustrate?",
                "options": {
                    "A": "Networked",
                    "B": "Duplicated",
                    "C": "Centralized",
                    "D": "Decentralized"
                },
                "ans": "A",
                "pdf_page": 37,
                "topic": "Global Systems Configurations (Networked)",
                "solution": "In a networked systems configuration, software development, data storage, and operational processing are shared collaboratively across interconnected international nodes rather than controlled from a single hub."
            },
            {
                "num": 5,
                "text": "Which of the following activities falls under the category of 'back office functions'?",
                "options": {
                    "A": "Catering for railway passengers",
                    "B": "Advisory services for external clients",
                    "C": "Training and R&D",
                    "D": "Procurement of raw materials for production"
                },
                "ans": "C",
                "pdf_page": 37,
                "topic": "Back Office vs. Front Office Operations",
                "solution": "Back office operations comprise internal administrative, HR, infrastructure, training, and research & development activities that do not directly interface with external consumer clients."
            },
            {
                "num": 6,
                "text": "Match each concept (column A) with the correct description (column B): 1. Resource sharing, 2. Centralization of services, 3. Joint Venture, 4. Outsourcing.",
                "options": {
                    "A": "1–D, 2–B, 3–A, 4–C",
                    "B": "1–B, 2–A, 3–C, 4–D",
                    "C": "1–D, 2–B, 3–C, 4–A",
                    "D": "1–A, 2–B, 3–C, 4–D"
                },
                "ans": "C",
                "pdf_page": 38,
                "topic": "Global Sourcing & Service Delivery Models",
                "solution": "1-D: Resource sharing uses plant/personnel across countries. 2-B: Centralization relocates services to a single shared hub. 3-C: Joint Venture creates a separate entity. 4-A: Outsourcing shifts processes to third-party providers."
            },
            {
                "num": 7,
                "text": "During which transition activity are project records, manuals, and reports stored and handed over to the support team?",
                "options": {
                    "A": "Human resource transition",
                    "B": "Project documentation transition",
                    "C": "Infrastructure transition",
                    "D": "Financial transition"
                },
                "ans": "B",
                "pdf_page": 38,
                "topic": "IT Project Transition Activities",
                "solution": "The project documentation transition stream governs the formal handover of technical runbooks, architecture diagrams, user manuals, and maintenance logs to the ongoing support organization."
            },
            {
                "num": 8,
                "text": "Which of the following represents the correct categorization of a Continuous Improvement activity within an outsourced support framework?",
                "options": {
                    "A": "Root Cause Analysis",
                    "B": "Value Realization",
                    "C": "Evaluate learning effectiveness",
                    "D": "Deliver continuous End User Training"
                },
                "ans": "B",
                "pdf_page": 38,
                "topic": "Continuous Improvement & Value Realization",
                "solution": "In IT outsourcing governance, Value Realization is the disciplined continuous improvement practice of tracking and harvesting projected strategic and financial benefits beyond standard SLA compliance."
            },
            {
                "num": 9,
                "text": "Breakthroughs in transportation and telecommunication costs belong to which era of globalization?",
                "options": {
                    "A": "Globalization 1.0",
                    "B": "Globalization 2.0",
                    "C": "Globalization 3.0",
                    "D": "None of these"
                },
                "ans": "B",
                "pdf_page": 39,
                "topic": "Friedman's Eras of Globalization",
                "solution": "In Thomas Friedman's framework, Globalization 2.0 (1800 to 2000) was driven by multinational companies and technological breakthroughs in transportation (steam engines, rail) and communications (telegraph, telephone)."
            },
            {
                "num": 10,
                "text": "In the context of Thomas Friedman's 'Flat World' theory, how does 'In-forming' primarily benefit global corporations and individuals?",
                "options": {
                    "A": "By restricting public access to corporate data to maintain a competitive advantage.",
                    "B": "By replacing traditional human resources entirely with artificial intelligence.",
                    "C": "By automating the physical assembly and manufacturing of products in overseas factories.",
                    "D": "By providing everyone with the tools to build a personal information supply chain, democratising access to global knowledge."
                },
                "ans": "D",
                "pdf_page": 39,
                "topic": "Friedman's Flatteners: In-forming",
                "solution": "In-forming (Flattener #10) is exemplified by search engines like Google and digital libraries, empowering individuals to build their own supply chain of information, knowledge, and entertainment."
            }
        ]
    }
]

# -------------------------------------------------------------
# 3. Main Processing Logic
# -------------------------------------------------------------
def main():
    conn = sqlite3.connect('mis_questions.db')
    c = conn.cursor()

    # Step A: Clean existing 1,560 question stems in mis_questions.db
    print("Step 1: Cleaning slide/page mentions from 1,560 main questions...")
    c.execute("SELECT id, question FROM questions")
    main_rows = c.fetchall()
    cleaned_count = 0
    for q_id, q_text in main_rows:
        new_text = clean_question_stem(q_text)
        if new_text != q_text:
            c.execute("UPDATE questions SET question = ? WHERE id = ?", (new_text, q_id))
            cleaned_count += 1
    conn.commit()
    print(f"Successfully cleaned {cleaned_count} question stems in mis_questions.db!")

    # Step B: Create and populate assignment_questions table
    print("\nStep 2: Creating and populating assignment_questions table...")
    c.execute("""
    CREATE TABLE IF NOT EXISTS assignment_questions (
        id TEXT PRIMARY KEY,
        week INTEGER NOT NULL,
        question_num INTEGER NOT NULL,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        topic TEXT NOT NULL,
        solution TEXT NOT NULL,
        source_pdf_page INTEGER NOT NULL
    )
    """)
    c.execute("DELETE FROM assignment_questions")

    total_assignments = 0
    flat_assignments = []

    for week_data in ASSIGNMENTS_DATA:
        w_num = week_data["week"]
        for q in week_data["questions"]:
            q_id = f"MIS-ASSIGN-W{w_num:02d}-Q{q['num']:02d}"
            c.execute("""
            INSERT INTO assignment_questions (
                id, week, question_num, question,
                option_a, option_b, option_c, option_d,
                correct_answer, topic, solution, source_pdf_page
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                q_id, w_num, q["num"], q["text"],
                q["options"]["A"], q["options"]["B"], q["options"]["C"], q["options"]["D"],
                q["ans"], q["topic"], q["solution"], q["pdf_page"]
            ))
            flat_assignments.append({
                "assignment_id": q_id,
                "id": q_id,
                "week_number": w_num,
                "week": w_num,
                "question_number": q["num"],
                "question_text": q["text"],
                "question": q["text"],
                "options": q["options"],
                "option_a": q["options"]["A"],
                "option_b": q["options"]["B"],
                "option_c": q["options"]["C"],
                "option_d": q["options"]["D"],
                "correct_option": q["ans"],
                "correct_answer": q["ans"],
                "topic": q["topic"],
                "solution": q["solution"],
                "explanation": q["solution"],
                "source_pdf_page": q["pdf_page"]
            })
            total_assignments += 1

    conn.commit()
    print(f"Inserted {total_assignments} official assignment questions across 12 weeks!")

    # Step C: Save to public/data/assignments.json and public/exports/
    os.makedirs("public/data", exist_ok=True)
    os.makedirs("public/exports", exist_ok=True)

    with open("public/data/assignments.json", "w", encoding="utf-8") as f:
        json.dump(flat_assignments, f, indent=2, ensure_ascii=False)
    with open("public/exports/nptel_mis_assignments_120_mcqs.json", "w", encoding="utf-8") as f:
        json.dump(flat_assignments, f, indent=2, ensure_ascii=False)
    print("Saved public/data/assignments.json and export file!")

    # Step D: Update public/exports/mis_question_bank.json and .csv with cleaned stems
    conn.row_factory = sqlite3.Row
    c2 = conn.cursor()
    c2.execute("""
    SELECT 
        q.*,
        CASE WHEN b.question_id IS NOT NULL THEN 1 ELSE 0 END as is_bookmarked,
        b.note as bookmark_note
    FROM questions q
    LEFT JOIN bookmarks b ON q.id = b.question_id
    WHERE q.validation_status = 'VALIDATED'
    ORDER BY q.week, q.lecture_num, q.id
    """)
    updated_questions = [dict(r) for r in c2.fetchall()]

    with open("public/exports/mis_question_bank.json", "w", encoding="utf-8") as f:
        json.dump(updated_questions, f, indent=2, ensure_ascii=False)

    import csv
    if updated_questions:
        keys = list(updated_questions[0].keys())
        with open("public/exports/mis_question_bank.csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(updated_questions)
    print("Updated public/exports/mis_question_bank.json and .csv with cleaned question stems!")

    conn.close()
    print("\nALL TASKS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
