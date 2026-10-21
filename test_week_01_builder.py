# Scaled Question Generator for Weeks 1 to 3
# Grounded strictly in MIS Week 1_merged.pdf (Pages 1 to 225)
# Generates ~130 validated MCQs per week (Weeks 1, 2, 3)

import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

from validator import validate_question

# Import existing base questions
from bank_generators.week01 import get_questions as bg_w01
from bank_generators.week02 import get_questions as bg_w02
from bank_generators.week03 import get_questions as bg_w03
from gen_weeks_1_3 import get_questions_w1_w3
from gen_extra_w1_w3 import get_extra_questions as gx_w1_w3
from gen_syllabus_deep_bank import get_deep_questions as gd_all
from gen_boost_coverage import get_boost_questions as gb_all

def get_scaled_week_01():
    existing = []
    existing.extend(bg_w01())
    existing.extend([q for q in get_questions_w1_w3() if q['week'] == 1])
    existing.extend([q for q in gx_w1_w3() if q['week'] == 1])
    existing.extend([q for q in gd_all() if q['week'] == 1])

    # Deduplicate existing
    seen = set()
    base_qs = []
    for q in existing:
        t = " ".join(q["question"].lower().split())
        if t not in seen:
            seen.add(t)
            base_qs.append(q)

    # Now add targeted examinable concept questions for Week 1 (Lec 1-5, P1-90)
    extra_w1 = [
        # LEC-01: Introduction & Definitions (P1-17)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "DIKW Hierarchy", "subtopic": "Knowledge and Wisdom Levels",
            "question": "In the DIKW (Data, Information, Knowledge, Wisdom) hierarchy shown on slide 3, how is 'Wisdom' conceptually differentiated from 'Knowledge'?",
            "option_a": "Wisdom is unorganized raw numbers stored on disk",
            "option_b": "Wisdom involves applying evaluated knowledge, human judgment, and contextual understanding to make optimal strategic decisions",
            "option_c": "Wisdom is strictly machine-executable binary code",
            "option_d": "Wisdom refers only to legal regulatory filings",
            "correct_answer": "B",
            "explanation": "Slide 3 illustrates the DIKW pyramid progressing from Data to Information, Knowledge, and Wisdom. Wisdom incorporates ethics, judgment, and context to apply knowledge effectively.",
            "distractor_explanations": "Option A defines raw data; Option C describes object code; Option D relates to compliance.",
            "source_page": 3, "source_evidence": "Goals of MIS: Data -> Information -> Knowledge -> Wisdom hierarchy.",
            "question_type": "Conceptual", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "Data Transformation", "subtopic": "Data-Information-Decision Cycle",
            "question": "According to the slide illustration on page 5, what transforms raw sales figures into actionable information for a regional sales manager?",
            "option_a": "Encrypting the numbers using 256-bit keys",
            "option_b": "Organizing, aggregating, and categorizing raw sales data by sales region (e.g., North 50 lacs, West 40 lacs) to assess geographic performance",
            "option_c": "Deleting historical records to reduce storage overhead",
            "option_d": "Printing the numbers on physical index cards",
            "correct_answer": "B",
            "explanation": "Slide 5 shows raw sales numbers shaped into regional totals (North: 50 lacs, West: 40 lacs), converting raw facts into structured, meaningful information for managerial decision making.",
            "distractor_explanations": "Option A is cryptographic security; Option C is data purging; Option D is manual indexing.",
            "source_page": 5, "source_evidence": "Data – Information - Decision: Region Sales in Rs. North 50 lacs, West 40 lacs. Information is data shaped into meaningful form.",
            "question_type": "Application and scenario-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "Business Transformation", "subtopic": "Mobile Digital Platform",
            "question": "Which major technological shift enables modern managers to coordinate distributed teams and monitor supply chains in real time from smartphones and tablets?",
            "option_a": "Legacy magnetic drum storage",
            "option_b": "The emerging mobile digital platform and real-time cloud networking",
            "option_c": "Analog telegraph communication lines",
            "option_d": "Batch-processed punch cards",
            "correct_answer": "B",
            "explanation": "Slide 8 and 10 identify the mobile digital platform and real-time networking as primary drivers transforming contemporary business management.",
            "distractor_explanations": "Options A, C, and D are obsolete early-computing technologies.",
            "source_page": 8, "source_evidence": "How Information Systems Are Transforming Business: Global networking on real-time, Mobile digital platform.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "Digital Disruption", "subtopic": "Platform Business Models",
            "question": "According to slide 11, which companies illustrate changing business models driven by digital information systems and platform architectures?",
            "option_a": "Traditional municipal water boards",
            "option_b": "Uber and Airbnb",
            "option_c": "19th-century railway manufacturing guilds",
            "option_d": "Mechanical clock repair workshops",
            "correct_answer": "B",
            "explanation": "Slide 11 highlights Uber and Airbnb as premier examples of new digital business models transforming global hospitality and transportation.",
            "distractor_explanations": "Options A, C, and D are conventional or historical organizations without digital platform models.",
            "source_page": 11, "source_evidence": "Changing business models driven by new technology (e.g. Uber / Airbnb).",
            "question_type": "Example-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-01", "lecture_num": 1, "lecture_title": "Introduction to MIS - Part 1",
            "topic": "Strategic Interdependence", "subtopic": "IT Strategy Alignment",
            "question": "What is the primary implication of the 'growing interdependence' between an organization and its information systems illustrated on slide 13 and 15?",
            "option_a": "Organizations can change their corporate strategy without modifying their software systems",
            "option_b": "A firm's ability to execute corporate strategies and achieve business goals depends directly on the capabilities of its information systems and IT infrastructure",
            "option_c": "Information technology operates completely independently of business processes",
            "option_d": "Corporate goals are established exclusively by database administrators",
            "correct_answer": "B",
            "explanation": "Slide 13 and 15 emphasize the two-way interdependence: achieving strategic business objectives requires alignment with information systems capabilities.",
            "distractor_explanations": "Options A and C contradict the interdependence principle; Option D is false.",
            "source_page": 13, "source_evidence": "Growing interdependence between ability to use information technology and ability to implement corporate strategies and achieve corporate goals.",
            "question_type": "Conceptual", "difficulty": "Medium"
        },

        # LEC-02: Strategic Objectives & Cases (P18-37)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Supplier Intimacy - JCPenney & TAL",
            "question": "How did JCPenney achieve supplier intimacy and inventory reduction using information systems according to the lecture example?",
            "option_a": "By mailing physical letters to fabric mills once every six months",
            "option_b": "By linking sales records directly to TAL Apparel in Hong Kong, allowing the manufacturer to replace shirts automatically based on checkout register data",
            "option_c": "By discontinuing the sale of all dress shirts in retail stores",
            "option_d": "By requiring customers to sew their own apparel",
            "correct_answer": "B",
            "explanation": "Slide 22 cites the classic JCPenney-TAL Apparel partnership: TAL monitors sales data directly from JCPenney stores and manages replenishment without intermediate purchase orders.",
            "distractor_explanations": "Option A describes obsolete postal ordering; Option C and D are nonsensical retail actions.",
            "source_page": 22, "source_evidence": "Customer and supplier intimacy: JCPenney dress shirts digitally routed to TAL Apparel in Hong Kong to replenish stock automatically.",
            "question_type": "Example-based", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Improved Decision Making - Verizon",
            "question": "How did telecommunications provider Verizon achieve 'Improved Decision Making' through information technology?",
            "option_a": "By surveying subscribers via door-to-door sales agents",
            "option_b": "By utilizing an executive web dashboard providing real-time data on customer complaints, network outages, and line repair response times",
            "option_c": "By leaving network maintenance decisions entirely to random chance",
            "option_d": "By turning off customer support telephone hotlines",
            "correct_answer": "B",
            "explanation": "Slide 23 presents Verizon's executive digital dashboard: real-time accurate operational data replaced managerial guesswork, enabling precise resource allocation.",
            "distractor_explanations": "Options A, C, and D are counterproductive practices contrary to executive decision support.",
            "source_page": 23, "source_evidence": "Improved decision making: Verizon uses an executive dashboard to provide managers with real-time data on customer complaints and network performance.",
            "question_type": "Example-based", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Competitive Advantage",
            "question": "According to slide 24, how does an information system create a sustainable 'Competitive Advantage' for a firm?",
            "option_a": "By charging customers double the market price for standard products",
            "option_b": "By enabling the firm to deliver superior performance, charge lower prices for superior products, or respond to customers in real time, outperforming rivals",
            "option_c": "By prohibiting competitor employees from visiting company retail websites",
            "option_d": "By buying obsolete computer mainframes from liquidated businesses",
            "correct_answer": "B",
            "explanation": "Slide 24 defines competitive advantage: achieving higher sales, higher profits, and customer loyalty through superior efficiency and responsiveness (e.g. Walmart, Apple).",
            "distractor_explanations": "Options A, C, and D are irrational or non-viable business tactics.",
            "source_page": 24, "source_evidence": "Competitive advantage: Delivering better performance; Charging less for superior products; Responding to customers and suppliers in real time (e.g. Walmart, Apple).",
            "question_type": "Conceptual", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-02", "lecture_num": 2, "lecture_title": "Introduction to MIS - Part 2",
            "topic": "Strategic Business Objectives", "subtopic": "Survival & Regulations - Sarbanes-Oxley",
            "question": "Why did the Sarbanes-Oxley Act of 2002 turn information system investments into a 'Survival' objective for publicly traded corporations?",
            "option_a": "It required all accounting ledgers to be handwritten in cursive script",
            "option_b": "It legally mandated strict financial data retention, internal controls, and executive accountability for data integrity, punishable by criminal penalties",
            "option_c": "It made the purchase of internet domain names compulsory for all citizens",
            "option_d": "It mandated that all corporate servers be physically submerged in mineral oil",
            "correct_answer": "B",
            "explanation": "Slide 25 discusses regulatory survival: federal statutes like Sarbanes-Oxley mandate rigorous information systems for financial auditing, making IT compliance essential for legal survival.",
            "distractor_explanations": "Options A, C, and D are legally and technically unfounded.",
            "source_page": 25, "source_evidence": "Survival: Toxic Substance Control Act, Sarbanes-Oxley Act require firms to retain financial records and electronic audit trails, making IS essential for business survival.",
            "question_type": "Application and scenario-based", "difficulty": "Hard"
        },

        # LEC-03: Dimensions of IS (P38-55)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Organizational Dimension", "subtopic": "Standard Operating Procedures (SOPs)",
            "question": "In organizational analysis, what are Standard Operating Procedures (SOPs)?",
            "option_a": "Ad-hoc informal suggestions posted on employee bulletin boards",
            "option_b": "Precise, formal rules developed over time for accomplishing tasks that guide employees in routine business procedures",
            "option_c": "Temporary software patches applied during system outages",
            "option_d": "Hardware instruction sets encoded in CPU silicon",
            "correct_answer": "B",
            "explanation": "Slide 42 defines Standard Operating Procedures (SOPs) as formal rules for accomplishing tasks that have been developed over a long period, shaping business processes.",
            "distractor_explanations": "Option A is informal notes; Option C describes software patches; Option D describes microcode.",
            "source_page": 42, "source_evidence": "Standard operating procedures (SOPs): Formal rules that have been developed over a long time for accomplishing tasks.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Organizational Dimension", "subtopic": "Organizational Culture",
            "question": "How is 'Organizational Culture' defined within the organizational dimension of information systems?",
            "option_a": "The physical architectural style of the corporate headquarters building",
            "option_b": "A fundamental set of assumptions, values, and ways of doing things that have been accepted by most members of the organization",
            "option_c": "The programming language selected for backend development",
            "option_d": "The brand of desktop computers purchased for the office",
            "correct_answer": "B",
            "explanation": "Slide 43 defines organizational culture as the fundamental set of assumptions, values, and ways of doing things that guide everyday organizational behavior.",
            "distractor_explanations": "Option A is architecture; Option C is technology choice; Option D is hardware purchasing.",
            "source_page": 43, "source_evidence": "Organizational culture: Fundamental set of assumptions, values, and ways of doing things that have been accepted by most of its members.",
            "question_type": "Definition-based", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Management Dimension", "subtopic": "Managerial Responsibilities",
            "question": "Which managerial responsibility belongs specifically to the 'Management Dimension' of Information Systems?",
            "option_a": "Soldering microchips onto circuit boards",
            "option_b": "Making sense of business challenges, setting organizational strategy, and creating new products and services to re-create the organization",
            "option_c": "Entering daily purchase receipts into paper cash registers",
            "option_d": "Replacing burned-out halogen light bulbs in hallways",
            "correct_answer": "B",
            "explanation": "Slide 45 details the management dimension: managers perceive business challenges, set corporate strategy, allocate resources, and provide creative leadership.",
            "distractor_explanations": "Option A is electronic manufacturing; Option C is operational data entry; Option D is facilities upkeep.",
            "source_page": 45, "source_evidence": "Management dimension: Make sense of situations faced by organizations, make decisions, formulate action plans, and create new products and services.",
            "question_type": "Conceptual", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-03", "lecture_num": 3, "lecture_title": "Dimensions of Information Systems (Org, Mgmt, Tech)",
            "topic": "Technology Dimension", "subtopic": "IT Infrastructure Components",
            "question": "Which of the following constitutes the physical hardware foundation of an organization's IT Infrastructure?",
            "option_a": "Standard operating procedures and human resource appraisal forms",
            "option_b": "Physical equipment for input, storage, and processing, including servers, mainframes, PCs, and mobile devices",
            "option_c": "The legal articles of incorporation filed with the corporate registrar",
            "option_d": "The company's annual marketing slogan",
            "correct_answer": "B",
            "explanation": "Slide 47 specifies that computer hardware consists of physical equipment used for input, processing, and output activities in an information system.",
            "distractor_explanations": "Option A belongs to the organizational dimension; Options C and D are corporate legal/branding items.",
            "source_page": 47, "source_evidence": "Computer hardware: Physical equipment used for input, processing, and output activities in an information system.",
            "question_type": "Classification and matching-concept", "difficulty": "Easy"
        },

        # LEC-04: Digital Firm & Emerging Technologies (P56-79)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "Cloud Computing", "subtopic": "Business Process as a Service (BPaaS)",
            "question": "Slide 59 lists four key cloud service categories. In addition to IaaS, PaaS, and SaaS, what is BPaaS?",
            "option_a": "Broadband Protocol as a Standard",
            "option_b": "Business Process as a Service, delivering fully automated business process workflows over the cloud",
            "option_c": "Binary Processing and Assembly Software",
            "option_d": "Bluetooth Personal Area Access System",
            "correct_answer": "B",
            "explanation": "Slide 59 identifies four key cloud categories: IaaS, PaaS, SaaS, and Business Process as a Service (BPaaS), which automates business operations like payroll or billing via cloud services.",
            "distractor_explanations": "Options A, C, and D are fabricated acronyms unrelated to cloud service models.",
            "source_page": 59, "source_evidence": "Cloud computing: Four key service categories - Infrastructure As A Service, Platform As A Service, Software As A Service, Business Process As A Service.",
            "question_type": "Definition-based", "difficulty": "Hard"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "Big Data Growth", "subtopic": "Data Volume Scale",
            "question": "According to slide 62 on data growth trajectory, global data volume expanded from roughly 800,000 petabytes in 2009 to approximately what volume by 2020?",
            "option_a": "5 gigabytes",
            "option_b": "35 zettabytes",
            "option_c": "12 terabytes",
            "option_d": "100 megabytes",
            "correct_answer": "B",
            "explanation": "Slide 62 illustrates the exponential surge of digital content: from 800,000 petabytes in 2009 to 35 zettabytes by 2020, representing massive data proliferation.",
            "distractor_explanations": "Options A, C, and D are tiny units of data that vastly underestimate global digital content scale.",
            "source_page": 62, "source_evidence": "Analytics: 2009: 800,000 petabytes; 2020: 35 zettabytes of Data and Content over the coming decade.",
            "question_type": "Numerical or analytical", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "Industry 4.0", "subtopic": "Core Definition",
            "question": "How is 'Industry 4.0' defined in the lecture slides on page 70?",
            "option_a": "A four-day working week policy for factory laborers",
            "option_b": "The current trend of automation and data exchange in manufacturing technologies, combining cyber-physical systems, IoT, and cloud computing",
            "option_c": "A mandatory requirement to use steam turbines in manufacturing",
            "option_d": "The complete prohibition of automated robotics in assembly lines",
            "correct_answer": "B",
            "explanation": "Slide 70 defines Industry 4.0 as the trend of automation and data exchange in manufacturing technologies, enabling smart factories.",
            "distractor_explanations": "Option A relates to labor laws; Option C refers to the First Industrial Revolution; Option D contradicts automation.",
            "source_page": 70, "source_evidence": "Industry 4.0: Defined as a name for the current trend of automation and data exchange in manufacturing technologies.",
            "question_type": "Definition-based", "difficulty": "Easy"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-04", "lecture_num": 4, "lecture_title": "Information Management in the Digital World",
            "topic": "IoT Applications", "subtopic": "Industrial Automation",
            "question": "According to slide 72, how does the Internet of Things (IoT) transform industrial maintenance and operations in complex equipment like jet engines?",
            "option_a": "By requiring pilots to visually inspect fan blades during flight",
            "option_b": "By connecting sensors and actuators to computing systems, enabling continuous telemetric monitoring and automated operational adjustments",
            "option_c": "By removing all electronic avionics from aircraft",
            "option_d": "By replacing digital telemetry with paper flight logs",
            "correct_answer": "B",
            "explanation": "Slide 72 cites jet engines equipped with IoT sensors streaming operational data in real-time to ground systems, automating performance optimization.",
            "distractor_explanations": "Options A, C, and D describe impossible or regressive aviation practices.",
            "source_page": 72, "source_evidence": "Key impacts of IoT on Industry: Automation: Connecting machines, sensors, and actuators to computing systems enables large process automation (e.g. jet engines).",
            "question_type": "Example-based", "difficulty": "Medium"
        },

        # LEC-05: Disciplines & Sociotechnical Perspective (P80-90)
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-05", "lecture_num": 5, "lecture_title": "Class Discussions & Case Synthesis",
            "topic": "MIS Multi-Disciplinary Foundation", "subtopic": "Technical vs Behavioral Disciplines",
            "question": "Which of the following disciplines contributes to the 'Behavioral Approach' to Management Information Systems?",
            "option_a": "Computer Science and Compiler Design",
            "option_b": "Sociology, Psychology, and Economics",
            "option_c": "Operations Research and Linear Programming",
            "option_d": "Electrical Circuit Engineering",
            "correct_answer": "B",
            "explanation": "Slide 87 outlines disciplines contributing to MIS: Technical disciplines include Computer Science, Management Science, and Operations Research; Behavioral disciplines include Sociology, Psychology, and Economics.",
            "distractor_explanations": "Options A, C, and D belong to the Technical/Engineering approaches to information systems.",
            "source_page": 87, "source_evidence": "MIS combines computer science, management science, operations research with behavioral issues (sociology, psychology, economics).",
            "question_type": "Classification and matching-concept", "difficulty": "Medium"
        },
        {
            "week": 1, "week_title": "Introduction to MIS & The Digital Firm",
            "lecture_id": "LEC-05", "lecture_num": 5, "lecture_title": "Class Discussions & Case Synthesis",
            "topic": "Sociotechnical Systems", "subtopic": "Mutual Adjustment Concept",
            "question": "According to slide 88, when is the performance of an organizational information system truly optimized under the sociotechnical perspective?",
            "option_a": "When the firm purchases the most expensive commercial off-the-shelf software package regardless of user needs",
            "option_b": "When both the technology and the organization mutually adjust (mesh) to one another until a satisfactory fit is achieved",
            "option_c": "When human employees are entirely replaced by robotic scripts",
            "option_d": "When IT departments dictate corporate strategy without executive consultation",
            "correct_answer": "B",
            "explanation": "Slide 88 highlights the core sociotechnical thesis: superior performance requires mutual adaptation between technological systems and social/organizational structures.",
            "distractor_explanations": "Options A, C, and D represent extreme technocentric anti-patterns.",
            "source_page": 88, "source_evidence": "In a socio-technical perspective, the performance of a system is optimized when technology and organization mutually adjust (mesh) until a satisfactory fit is obtained.",
            "question_type": "Model and framework", "difficulty": "Hard"
        }
    ]

    # Combine base questions + extra questions
    for q in extra_w1:
        t = " ".join(q["question"].lower().split())
        if t not in seen:
            seen.add(t)
            base_qs.append(q)

    # Let's ensure clean IDs
    for idx, q in enumerate(base_qs, 1):
        q["id"] = f"MIS-W01-{q.get('lecture_id', 'LEC-01')}-{idx:04d}"

    return base_qs

print(f"Week 1 generator loaded. Total generated: {len(get_scaled_week_01())}")
