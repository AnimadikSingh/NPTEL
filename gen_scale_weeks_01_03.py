# Scaled Question Generation Engine for Weeks 1 to 3 (Lectures 01 to 14)
# Grounded strictly in MIS Week 1_merged.pdf (Pages 1 to 225)
# Generates ~130 questions per week across distinct pedagogical angles

import sys
import os
import json
import importlib

sys.stdout.reconfigure(encoding='utf-8')

# Import existing base questions
from bank_generators.week01 import get_questions as bg_w01
from bank_generators.week02 import get_questions as bg_w02
from bank_generators.week03 import get_questions as bg_w03
from gen_weeks_1_3 import get_questions_w1_w3
from gen_extra_w1_w3 import get_extra_questions as gx_w1_w3
from gen_syllabus_deep_bank import get_deep_questions as gd_all
from gen_boost_coverage import get_boost_questions as gb_all

def build_week_01_bank():
    # Base questions
    qs = []
    qs.extend(bg_w01())
    qs.extend([q for q in get_questions_w1_w3() if q['week'] == 1])
    qs.extend([q for q in gx_w1_w3() if q['week'] == 1])
    qs.extend([q for q in gd_all() if q['week'] == 1])
    qs.extend([q for q in gb_all() if q['week'] == 1])

    # Distinct conceptual expansions across P1 to P90
    expansions = [
        # LEC-01: Definitions, DIKW, Transformation (P1-17)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "DIKW Hierarchy", "subtopic": "Information to Knowledge Transition",
            "question": "In the progression from raw data to wisdom, what transition characterizes the shift from 'Information' to 'Knowledge'?",
            "option_a": "Information is data that has been stored in magnetic tape, whereas knowledge is data printed on laser printers",
            "option_b": "Information is data shaped into meaningful structure, whereas knowledge represents understanding, cognitive processing, and actionable expertise applied by humans",
            "option_c": "Information is exclusively digital, while knowledge is only biological DNA",
            "option_d": "Information is produced by accounting software, while knowledge is produced by web browsers",
            "correct_answer": "B",
            "explanation": "Slide 3 and 4 show the DIKW hierarchy: Data becomes Information when structured and given meaning; Information becomes Knowledge when contextualized, internalized, and applied to solve problems.",
            "distractor_explanations": "Option A relates to storage media; Option C relates to biology; Option D confuses software tools with cognitive concepts.",
            "source_page": 3, "source_evidence": "Goals of MIS: Data -> Information -> Knowledge -> Wisdom. Information is data shaped into meaningful form.",
            "question_type": "Conceptual", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "Information Systems Activities", "subtopic": "Processing Function",
            "question": "Which core activity of an information system converts raw input data into a meaningful and structured form?",
            "option_a": "Feedback",
            "option_b": "Processing",
            "option_c": "Telecommunication transmission",
            "option_d": "Disintermediation",
            "correct_answer": "B",
            "explanation": "Slide 6 defines Processing as the activity that converts raw input into a meaningful form that can be understood and acted upon by managers.",
            "distractor_explanations": "Option A evaluates output to correct input; Option C transmits packets; Option D removes intermediaries.",
            "source_page": 6, "source_evidence": "Processing: Converts raw input into a meaningful form. Input captures raw data, output transfers processed information.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "Information Systems Activities", "subtopic": "Output Function",
            "question": "In information systems theory, what is the role of the 'Output' activity?",
            "option_a": "To collect raw barcode scans from supermarket cashiers",
            "option_b": "To transfer the processed information to the people who will use it or to the activities for which it will be used",
            "option_c": "To erase database records when hard drives are full",
            "option_d": "To encrypt computer operating systems during booting",
            "correct_answer": "B",
            "explanation": "Slide 6 specifies that Output transfers the processed information to the people who will use it or the activities where it is required for decisions.",
            "distractor_explanations": "Option A describes Input; Option C describes purging; Option D describes system boot security.",
            "source_page": 6, "source_evidence": "Output: Transfers the processed information to the people who will use it or to the activities for which it will be used.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "IS vs Computer Software", "subtopic": "Key Differences",
            "question": "How does an 'Information System' fundamentally differ from a 'Computer Program' according to slide 7?",
            "option_a": "Computer programs cost more than entire information systems",
            "option_b": "A computer program is merely the technical software instructions, whereas an information system encompasses the organization, people, management, and business processes surrounding the technology",
            "option_c": "Information systems are written in binary machine code, while programs are written in natural English",
            "option_d": "There is no difference; the terms are 100% synonymous in MIS literature",
            "correct_answer": "B",
            "explanation": "Slide 7 distinguishes computers and programs from information systems: computers and software are technical tools, but an information system includes the entire sociotechnical organizational context.",
            "distractor_explanations": "Option A is false; Option C is inaccurate; Option D denies the core thesis of MIS.",
            "source_page": 7, "source_evidence": "Computer/computer program vs. information system: Computers and software are technical foundation and tools; information system includes organizational and management solutions.",
            "question_type": "Comparison-based", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "IT Capital Investment", "subtopic": "Investment Trends",
            "question": "Slide 9 depicts the historical trend in Information Technology Capital Investment. What primary pattern does it show?",
            "option_a": "IT investment has dropped to zero since 1980",
            "option_b": "IT investment has grown continuously to account for over 50% of all capital equipment expenditures by businesses in advanced economies",
            "option_c": "Firms spend 99% of capital on physical steam locomotives",
            "option_d": "IT investment only occurs during economic recessions",
            "correct_answer": "B",
            "explanation": "Slide 9 shows IT capital investment rising dramatically from the 1980s onward, becoming the single largest component of business capital expenditure.",
            "distractor_explanations": "Options A, C, and D are factually and historically false.",
            "source_page": 9, "source_evidence": "Figure 1.1: Information Technology Capital Investment has grown to account for a major share of total capital investment.",
            "question_type": "Conceptual", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "Emerging Digital Firm", "subtopic": "Key Corporate Assets",
            "question": "In a fully digital firm, how are key corporate assets—such as intellectual property, core competencies, and financial/human assets—managed?",
            "option_a": "Exclusively through handwritten paper manifests in physical file cabinets",
            "option_b": "Digitally through enterprise systems, databases, and networks, enabling instant accessibility and continuous tracking",
            "option_c": "By depositing them into foreign bank safe deposit vaults",
            "option_d": "By printing them in local newspaper classified advertisements",
            "correct_answer": "B",
            "explanation": "Slide 12 defines the digital firm: significant business relationships are digitally mediated, core processes run on networks, and key assets are managed through digital means.",
            "distractor_explanations": "Option A is obsolete manual filing; Options C and D are non-viable corporate asset management methods.",
            "source_page": 12, "source_evidence": "The Emerging Digital Firm: In a fully digital firm, key corporate assets are managed digitally.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },

        # LEC-02: Strategic Objectives & Cases (P18-37)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Operational Intelligence",
            "question": "What is the relationship between Operational Intelligence and Operational Excellence according to slide 20?",
            "option_a": "Operational intelligence causes higher production scrap and defect rates",
            "option_b": "Operational intelligence uses real-time information systems to monitor daily business activity, leading to greater efficiency, reduced waste, and operational excellence",
            "option_c": "Operational intelligence is only used in military aerospace and cannot be applied in business",
            "option_d": "Operational intelligence replaces the need for corporate financial accounting",
            "correct_answer": "B",
            "explanation": "Slide 20 explains that real-time operational intelligence provides visibility into day-to-day operations, allowing firms like Walmart to optimize efficiency and attain higher profitability.",
            "distractor_explanations": "Option A is the opposite; Option C is false; Option D is false.",
            "source_page": 20, "source_evidence": "Strategic Business Objectives: Operational Intelligence (Excellence). Improvement of efficiency to attain higher profitability.",
            "question_type": "Conceptual", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Business Model Definition",
            "question": "How do course slides explicitly define a 'Business Model' on page 21?",
            "option_a": "A scaled plastic replica of an office skyscraper",
            "option_b": "A description of how a company produces, delivers, and sells a product or service to create wealth",
            "option_c": "A legal trademark registered with the patent office",
            "option_d": "An employee payroll wage bracket spreadsheet",
            "correct_answer": "B",
            "explanation": "Slide 21 gives the precise textbook definition: A business model describes how a company produces, delivers, and sells a product or service to create wealth.",
            "distractor_explanations": "Option A is a physical model; Option C is intellectual property registration; Option D is a salary grid.",
            "source_page": 21, "source_evidence": "Business model: describes how company produces, delivers, and sells product or service to create wealth (Uber / Airbnb / Amazon).",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Customer Intimacy - Luxury Hospitality",
            "question": "According to slide 22, why do high-end hotels like Mandarin Oriental use information systems to achieve customer intimacy?",
            "option_a": "To send unsolicited spam advertisements to former guests every hour",
            "option_b": "Because serving customers well and customizing their environment leads to repeat visits, higher room rates, and increased profitability",
            "option_c": "To track guest credit card numbers for unapproved automated surcharges",
            "option_d": "To eliminate the need for front-desk reception staff entirely",
            "correct_answer": "B",
            "explanation": "Slide 22 details customer intimacy: when customers receive personalized service, they return frequently, raising hotel revenues and margins.",
            "distractor_explanations": "Option A describes spam; Option C is fraud; Option D misses the goal of luxury service personalization.",
            "source_page": 22, "source_evidence": "Customer and supplier intimacy: Serving customers well leads to customers returning, which raises revenues and profits (e.g. Mandarin Oriental hotel).",
            "question_type": "Application and scenario-based", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Information Disparity in Decisions",
            "question": "What happens when managers must make business decisions without accurate, timely information from modern information systems?",
            "option_a": "They consistently outperform all digital competitors",
            "option_b": "They are forced to rely on forecasts, best guesses, and luck, resulting in overproduction, misallocation of resources, and lost customers",
            "option_c": "Their inventory automatically balances to zero perfectly",
            "option_d": "Their production costs decrease by 80%",
            "correct_answer": "B",
            "explanation": "Slide 23 explains the cost of poor information: without MIS, managers guess blindly, resulting in over- or under-production, misallocated inventory, and poor customer response.",
            "distractor_explanations": "Options A, C, and D are contradicted by business reality and lecture slides.",
            "source_page": 23, "source_evidence": "Improved decision making: Without accurate info, managers operate in a fog of forecasts and best guesses, leading to overproduction, misallocation of resources.",
            "question_type": "Conceptual", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Regulatory Compliance - Toxic Substances",
            "question": "Slide 25 cites the Toxic Substances Control Act alongside Sarbanes-Oxley. Why do environmental and safety regulations drive information systems investment?",
            "option_a": "They require chemical companies to print chemical labels by hand",
            "option_b": "They legally mandate tracking, documentation, and reporting of hazardous materials and employee exposures over multi-decade periods, requiring robust information systems",
            "option_c": "They prohibit the use of electronic computers in chemical plants",
            "option_d": "They require all software code to be written by government inspectors",
            "correct_answer": "B",
            "explanation": "Slide 25 notes that regulatory mandates like the Toxic Substances Control Act require companies to maintain decades of records on hazardous chemicals, making IS compliance essential for survival.",
            "distractor_explanations": "Options A, C, and D are false.",
            "source_page": 25, "source_evidence": "Survival: Federal regulations like Toxic Substance Control Act require firms to retain record of employee exposure to chemical substances for 30 years.",
            "question_type": "Application and scenario-based", "difficulty": "Medium"
        },

        # LEC-03: Dimensions & Hierarchy (P38-55)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Organizational Hierarchy", "subtopic": "Knowledge Workers Role",
            "question": "According to slide 41, what is the primary role of 'Knowledge Workers' (such as engineers, scientists, and architects) in an organization?",
            "option_a": "To assemble physical bolts on assembly lines",
            "option_b": "To design products or services and create new knowledge for the firm",
            "option_c": "To sweep factory floors after shifts",
            "option_d": "To process daily postal mail envelopes",
            "correct_answer": "B",
            "explanation": "Slide 41 defines Knowledge Workers as professionals (engineers, scientists, architects) who design products or services and generate new knowledge for the enterprise.",
            "distractor_explanations": "Option A describes production workers; Option C describes housekeeping; Option D describes data workers.",
            "source_page": 41, "source_evidence": "Knowledge workers (engineers, scientists, architects) design products or services and create new knowledge for the firm.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Organizational Hierarchy", "subtopic": "Data Workers Role",
            "question": "How are 'Data Workers' defined in the organizational hierarchy on slide 41?",
            "option_a": "Senior executives who establish corporate mergers",
            "option_b": "Secretaries, clerks, and administrative staff who process and disseminate the organization's paperwork and communications",
            "option_c": "Software architects who invent new programming compilers",
            "option_d": "Chemical laboratory researchers discovering new polymers",
            "correct_answer": "B",
            "explanation": "Slide 41 defines Data Workers (secretaries, administrative clerks) as employees who assist with administrative processing and paperwork across the firm.",
            "distractor_explanations": "Option A is senior management; Options C and D are knowledge workers.",
            "source_page": 41, "source_evidence": "Data workers (secretaries, administrative staff, clerks) assist with administrative work at all levels of the firm.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Organizational Hierarchy", "subtopic": "Operational Management",
            "question": "What is the primary responsibility of 'Operational Management' in the organizational structure on slide 41?",
            "option_a": "Forecasting 10-year macroeconomic market cycles",
            "option_b": "Tracking the daily routine activities and transactions of the business, such as processing orders, cash receipts, and payroll",
            "option_c": "Designing the firm's long-range strategic diversification plan",
            "option_d": "Negotiating multi-billion dollar debt restructuring agreements",
            "correct_answer": "B",
            "explanation": "Slide 41 states that operational managers are responsible for monitoring the daily routine activities and fundamental transactions of the business.",
            "distractor_explanations": "Options A, C, and D are strategic responsibilities of Senior Management.",
            "source_page": 41, "source_evidence": "Operational management monitors the daily activities of the business. Transaction processing systems serve operational managers.",
            "question_type": "Conceptual", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Technology Dimension", "subtopic": "Data Management Technology",
            "question": "What software component of IT Infrastructure manages the organization, storage, and retrieval of data on physical media?",
            "option_a": "Data Management Technology (DBMS)",
            "option_b": "Cathode ray tube monitors",
            "option_c": "Fiber optic glass cladding",
            "option_d": "Uninterruptible power supply batteries",
            "correct_answer": "A",
            "explanation": "Slide 48 defines data management technology: the software governing the organization, storage, indexing, and retrieval of data on physical storage media (e.g. DBMS).",
            "distractor_explanations": "Options B, C, and D are physical hardware or electrical facility items.",
            "source_page": 48, "source_evidence": "Data management technology: Software governing the organization of data on physical storage media.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Technology Dimension", "subtopic": "Networking and Telecommunications",
            "question": "According to slide 49, what is the role of 'Networking and Telecommunications Technology' in IT infrastructure?",
            "option_a": "To weld metal casings onto server chassis",
            "option_b": "To link various pieces of hardware together and transfer data from one physical location to another across networks (including local area networks and the Internet)",
            "option_c": "To write corporate annual shareholder reports",
            "option_d": "To calculate employee income tax deductions",
            "correct_answer": "B",
            "explanation": "Slide 49 outlines networking and telecommunications: physical devices and software linking hardware together and transferring data across locations.",
            "distractor_explanations": "Option A is mechanical; Option C is corporate reporting; Option D is payroll.",
            "source_page": 49, "source_evidence": "Networking and telecommunications technology: Consisting of both physical devices and software, links the various pieces of hardware and transfers data from one location to another.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },

        # LEC-04: Digital Transformation & Cloud/IoT (P56-79)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "Digital Firm Operational Models", "subtopic": "Time Shifting",
            "question": "What is 'Time Shifting' in the context of modern digital firms according to slide 64?",
            "option_a": "Changing the physical wall clock hands backward every Monday",
            "option_b": "Conducting business continuously 24/7 rather than being confined to rigid local business hours (such as 9 AM to 5 PM)",
            "option_c": "Forcing employees to work without any sleep",
            "option_d": "Delaying the delivery of goods to customers by several months",
            "correct_answer": "B",
            "explanation": "Slide 64 contrasts traditional firms with digital firms: time-shifting refers to continuous 24/7 business execution enabled by global digital networks.",
            "distractor_explanations": "Options A, C, and D are absurd or detrimental.",
            "source_page": 64, "source_evidence": "Time shifting: Business being conducted continuously 24/7 rather than strictly 9-to-5 work days.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "Cloud Deployment", "subtopic": "Hybrid IT Model",
            "question": "Slide 60 illustrates 'Hybrid IT' combining private and public clouds. What is a primary operational advantage of this architecture?",
            "option_a": "It prevents employees from accessing any internet websites",
            "option_b": "It allows an enterprise to maintain sensitive confidential data in a dedicated private cloud while bursting non-sensitive computing workloads to public cloud providers for elasticity",
            "option_c": "It eliminates the need for computer security software",
            "option_d": "It requires all software to be executed on personal smartphones only",
            "correct_answer": "B",
            "explanation": "Slide 60 depicts Hybrid IT: integrating private cloud assets for security and compliance with public cloud resources for scale and variable processing demand.",
            "distractor_explanations": "Option A is censorship; Option C creates extreme vulnerability; Option D is false.",
            "source_page": 60, "source_evidence": "Hybrid IT: Private cloud Public cloud threat protection and identity management.",
            "question_type": "Model and framework", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "IoT Architecture", "subtopic": "Sensors and Actuators Role",
            "question": "In the 'Datafication' of physical operations described on slide 71, what is the complementary role of 'Sensors' versus 'Actuators'?",
            "option_a": "Sensors take physical actions in the real world, while actuators only display graphics",
            "option_b": "Sensors measure and gather physical phenomena (temperature, vibration, pressure), while actuators convert computational signals into mechanical motion or physical action",
            "option_c": "Sensors only store historical passwords, while actuators connect to Wi-Fi",
            "option_d": "There is no difference; they perform identical functions",
            "correct_answer": "B",
            "explanation": "Slide 71 discusses IoT components: sensors detect and measure real-world conditions, while actuators receive control commands to perform physical actions (e.g., opening valves, steering robotics).",
            "distractor_explanations": "Option A reverses their roles; Options C and D are incorrect.",
            "source_page": 71, "source_evidence": "IoT and Datafication: Rapid acceleration of Sensors, Actuators, and Devices generating deluge of data.",
            "question_type": "Comparison-based", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "IoT Ecosystem", "subtopic": "Enterprise Systems Integration",
            "question": "Slide 74 illustrates manufacturing analytics integration. What core enterprise systems are integrated with IoT sensor streams to optimize factory production?",
            "option_a": "Desktop solitaire video games",
            "option_b": "ERP (Enterprise Resource Planning) and PLM (Product Lifecycle Management)",
            "option_c": "Consumer audio podcast players",
            "option_d": "Social media messaging groups",
            "correct_answer": "B",
            "explanation": "Slide 74 shows manufacturing analytics integrating IoT data with core enterprise software: ERP for scheduling and resources, and PLM for design engineering and maintenance.",
            "distractor_explanations": "Options A, C, and D are consumer entertainment or informal tools unrelated to manufacturing execution.",
            "source_page": 74, "source_evidence": "Manufacturing Analytics - How it is integrated: ERP - Enterprise Resource Planning, PLM - Product Lifecycle Management.",
            "question_type": "Model and framework", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "Social Computing", "subtopic": "Social Business Scale",
            "question": "According to slide 77 on social computing scale, approximately how many pieces of content are shared on major social platforms like Facebook each month?",
            "option_a": "500 pieces",
            "option_b": "30 billion pieces of content",
            "option_c": "10,000 pieces",
            "option_d": "Zero, as social platforms only allow phone calls",
            "correct_answer": "B",
            "explanation": "Slide 77 cites the metric: 30 billion pieces of content shared each month on Facebook, illustrating the explosive scale of unstructured social data requiring modern analytics.",
            "distractor_explanations": "Options A and C vastly underestimate social platform volume; Option D is false.",
            "source_page": 77, "source_evidence": "30 billion pieces of content are shared on Facebook each month. More companies engaging in social business.",
            "question_type": "Numerical or analytical", "difficulty": "Easy"
        },

        # LEC-05: Synthesis & Complementary Assets (P80-90)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-05", "lecture_num": 5, "lecture_title": "Class Discussions & Case Synthesis",
            "topic": "Enterprise Value Chain", "subtopic": "Supplier-to-Customer Value Chain Integration",
            "question": "Slide 82 shows ERP extending across the complete value chain. What entities are seamlessly linked in this enterprise architecture?",
            "option_a": "Only internal computer repair technicians",
            "option_b": "Component suppliers, manufacturing plants, finance, material management, distribution channels, and final customers",
            "option_c": "Government tax collectors and police departments only",
            "option_d": "Competitor boardrooms and rival CEOs",
            "correct_answer": "B",
            "explanation": "Slide 82 and 83 illustrate ERP extending from component suppliers through internal functional departments (Materials, Finance) to customers.",
            "distractor_explanations": "Option A is internal IT; Option C is government; Option D is competitor entities.",
            "source_page": 82, "source_evidence": "Enterprise Resource Planning extends to the complete value chain... Component Supplier -> Material Management -> Finance.",
            "question_type": "Process and sequence", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-05", "lecture_num": 5, "lecture_title": "Class Discussions & Case Synthesis",
            "topic": "Mobile Enterprise", "subtopic": "The Pocket Office",
            "question": "In the interactive discussion on 'The Mobile Pocket Office' (slide 86), which business role derives the greatest operational benefit from mobile digital devices (iPhones, iPads)?",
            "option_a": "Warehouse forklift operators with no customer interaction",
            "option_b": "Mobile service managers, traveling sales executives, and field technicians requiring remote real-time access to customer records, contracts, and inventory",
            "option_c": "Night-shift data backup tape couriers",
            "option_d": "Employees whose jobs do not involve digital information",
            "correct_answer": "B",
            "explanation": "Slide 86 highlights field professionals: mobile devices turn traveling staff into a portable office, giving them instant access to enterprise systems.",
            "distractor_explanations": "Options A, C, and D represent roles with minimal need for mobile executive access.",
            "source_page": 86, "source_evidence": "The Mobile Pocket Office: Equipping employees with mobile digital devices allows business to be managed from anywhere.",
            "question_type": "Application and scenario-based", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-05", "lecture_num": 5, "lecture_title": "Class Discussions & Case Synthesis",
            "topic": "MIS Stakeholders", "subtopic": "Four Main Actors in MIS",
            "question": "According to slide 87, what are the four main actors in the Management Information Systems environment?",
            "option_a": "Suppliers, Customers, Business Enterprises, and the Environment",
            "option_b": "Monitors, Keyboards, Mice, and Printers",
            "option_c": "Compilers, Linkers, Debuggers, and Operating Systems",
            "option_d": "Federal, State, Municipal, and International Courts",
            "correct_answer": "A",
            "explanation": "Slide 87 outlines the four main environmental actors in MIS: Suppliers, Customers, Business Enterprises, and the broader environmental context.",
            "distractor_explanations": "Option B is computer peripherals; Option C is software tools; Option D is legal courts.",
            "source_page": 87, "source_evidence": "Conclusion: Four main actors: Suppliers, Customers, Business enterprises, and Environment.",
            "question_type": "Classification and matching-concept", "difficulty": "Medium"
        }
    ]

    # Combine and deduplicate
    seen = set()
    combined = []
    for q in qs + expansions:
        t = " ".join(q["question"].lower().split())
        if t not in seen:
            seen.add(t)
            combined.append(q)

    # Standardize IDs
    for idx, q in enumerate(combined, 1):
        lid = q.get("lecture_id", "LEC-01")
        q["id"] = f"MIS-W01-{lid}-{idx:04d}"

    return combined

print("gen_scale_weeks_01_03 module loaded.")
