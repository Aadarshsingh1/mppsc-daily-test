# -*- coding: utf-8 -*-
"""
MPPSC Previous-Year Question (PYQ) & Syllabus Pattern Analyzer
Codifies actual examination blueprints, historical question patterns,
and difficulty distribution based on official MPPSC State Services Prelims papers.
"""

from typing import Dict, List, Any

# Official MPPSC Prelims Paper-1 Syllabus Blueprint (10 Units)
MPPSC_SYLLABUS_BLUEPRINT = {
    "Unit 1": {
        "title_en": "History, Culture and Literature of Madhya Pradesh",
        "title_hi": "मध्य प्रदेश का इतिहास, संस्कृति एवं साहित्य",
        "weightage": 10,
        "key_themes": [
            "Major historical dynasties (Parmara, Chandela, Bundela, Holkar, Scindia, Gond)",
            "Contribution of MP in freedom movement and 1857 revolt (Tatya Tope, Bheema Nayak, Shankar Shah)",
            "Major arts, sculpture, architecture (Khajuraho, Sanchi, Bhimbetka, Gwalior Fort)",
            "Tribal culture, dialects, festivals (Bhagoria Haat, Pithora painting, Mandana)",
            "Literary personalities of MP (Kalidasa, Bhavabhuti, Bhartrihari, Makhanlal Chaturvedi)",
            "Religious and tourist places of MP"
        ]
    },
    "Unit 2": {
        "title_en": "History of India",
        "title_hi": "भारत का इतिहास",
        "weightage": 10,
        "key_themes": [
            "Ancient India: Indus Valley, Vedic period, Mahajanapadas (Avanti), Mauryan and Gupta empire",
            "Medieval India: Delhi Sultanate administrative systems, Mughal administration, Bhakti/Sufi movements",
            "Modern India: British colonial acts (1813, 1833, 1858), socio-religious reform movements",
            "Indian National Movement: Gandhian satyagrahas (Champaran, Non-Cooperation, Civil Disobedience, Quit India)",
            "Tripuri Congress Session 1939 (near Jabalpur) and Subhas Chandra Bose"
        ]
    },
    "Unit 3": {
        "title_en": "Geography of Madhya Pradesh",
        "title_hi": "मध्य प्रदेश का भूगोल",
        "weightage": 10,
        "key_themes": [
            "Forests, forest produce, wildlife, national parks and sanctuaries (Kuno Project Cheetah, Kanha)",
            "Rivers of MP (Narmada origin, length in MP, Chambal, Betwa, Son, Tapti)",
            "Mountains and physiography (Satpura range, Dhupgarh peak, Malwa plateau)",
            "Climate of MP, seasons, rainfall distribution, Tropic of Cancer (14 districts)",
            "Soils of MP (Black soil, alluvial gully erosion in Chambal ravines)",
            "Major minerals (Copper in Malanjkhand, Manganese in Bharveli, Diamond in Panna)",
            "Major irrigation and multi-purpose river valley projects (Bargi, Gandhi Sagar, Indira Sagar)"
        ]
    },
    "Unit 4": {
        "title_en": "Geography of India and World",
        "title_hi": "भारत एवं विश्व का भूगोल",
        "weightage": 10,
        "key_themes": [
            "Physical features of India (Himalayan ranges, Northern Plains - Bhabhar, Terai, Bhangar, Khadar)",
            "Drainage systems (Himalayan vs Peninsular rivers, West-flowing vs East-flowing)",
            "Climate of India: Southwest monsoon mechanisms, Western Disturbances",
            "Natural resources, minerals (Gondwana coal reserves)",
            "World Geography: Continents, oceans, Ring of Fire, major straits (Malacca, Suez, Hormuz)",
            "Atmospheric layers (Troposphere, Stratosphere ozone layer) and ocean currents (Gulf Stream, Benguela)",
            "Ramsar wetland convention and MP sites (Bhoj wetland, Sirpur, Yashwant Sagar, Sakhya Sagar)"
        ]
    },
    "Unit 5": {
        "title_en": "Constitutional System and Economy of Madhya Pradesh",
        "title_hi": "मध्य प्रदेश की संवैधानिक व्यवस्था एवं अर्थव्यवस्था",
        "weightage": 10,
        "key_themes": [
            "Constitutional system of MP: Governor (first Governor Pattabhi Sitaramayya), Council of Ministers, Chief Minister",
            "Legislative Assembly of MP (230 seats: 47 ST, 35 SC reserved)",
            "High Court of MP (Principal Seat Jabalpur, permanent benches at Indore and Gwalior 1968)",
            "Three-tier Panchayati Raj and Urban Local Bodies (MP Panchayati Raj Act 1993, first state to hold elections)",
            "Demographics of MP (Census 2011 sex ratio 931, Balaghat highest 1021; literacy 69.32%)",
            "Economic development, GSDP sectoral contribution (Agriculture/Primary sector dominance)",
            "Major industries of MP (Pithampur - Detroit of India, BNP Dewas, Security Paper Mill)",
            "Tribal welfare programs and PESA Act implementation in MP (November 2022)"
        ]
    },
    "Unit 6": {
        "title_en": "Constitution, Governance and Economy of India",
        "title_hi": "भारत का संविधान, शासन प्रणाली एवं अर्थव्यवस्था",
        "weightage": 10,
        "key_themes": [
            "Constitutional history: Government of India Acts 1919 and 1935 (Provincial Autonomy)",
            "Constituent Assembly, Preamble, Fundamental Rights (Article 21, Article 32 Writs: Quo-Warranto, Mandamus)",
            "Directive Principles of State Policy (Article 40 Panchayats, Article 44 UCC)",
            "Union Executive: President of India (election, ordinance Art 123, pardon Art 72), Parliament (Money Bill Art 110)",
            "Judiciary: Supreme Court jurisdiction (Original Art 131, Advisory Art 143), Basic Structure doctrine (Kesavananda Bharati)",
            "Reserve Bank of India (RBI), Monetary Policy Committee (MPC 6 members), Repo Rate",
            "National economy: GST (101st Amendment, Article 279A), SEBI statutory status (1992 Act)"
        ]
    },
    "Unit 7": {
        "title_en": "Science, Technology and Environment",
        "title_hi": "विज्ञान एवं प्रौद्योगिकी, पर्यावरण तथा पारिस्थितिकी",
        "weightage": 10,
        "key_themes": [
            "Fundamental principles of science, acid rain (SO2 and NOx gases)",
            "Human body, hormones (Insulin from Beta cells of Pancreas), blood circulatory system",
            "Nutrition and deficiency diseases (Vitamin C scurvy, water-soluble vs fat-soluble vitamins)",
            "Space technology: ISRO satellite launch vehicles, Chandrayaan-3 (Shiv Shakti Point), National Space Day",
            "Defense technology: DRDO IGMDP program (Nag anti-tank missile, Agni, Prithvi)",
            "Ecosystem: Trophic levels, Lindeman's 10% energy transfer law, Biomagnification vs Bioaccumulation",
            "Biodiversity hotspots in India, Wildlife Protection Act 1972",
            "Renewable energy: International Solar Alliance (Gurugram HQ), Rewa Solar Project MP (750 MW)"
        ]
    },
    "Unit 8": {
        "title_en": "Current Events of State, National & International, Sports",
        "title_hi": "समसामयिक घटनाएं (मध्य प्रदेश, राष्ट्रीय एवं अंतर्राष्ट्रीय) तथा खेल",
        "weightage": 10,
        "key_themes": [
            "Major events of MP: 17th Pravasi Bharatiya Divas (Indore Jan 2023), Ladli Behna Yojana",
            "National current events: G20 New Delhi Summit 2023 ('Vasudhaiva Kutumbakam')",
            "International summits: BRICS expansion (Egypt, Ethiopia, Iran, Saudi Arabia, UAE from Jan 2024)",
            "Sports of MP: State sport Mallakhamb (declared 2013), Prabhash Joshi Award, Vishwamitra Award for coaches",
            "Major national games: Khelo India Youth Games (5th edition in MP across 8 cities)",
            "International sports: Asian Games Hangzhou (India 107 medals milestone), Arjuna Awardees (Divyakriti Singh equestrian)"
        ]
    },
    "Unit 9": {
        "title_en": "Information and Communication Technology (ICT)",
        "title_hi": "सूचना एवं संचार प्रौद्योगिकी",
        "weightage": 10,
        "key_themes": [
            "Computer networks: OSI reference model (7 layers, Network layer IP routing), IPv4 vs IPv6 (128-bit)",
            "Internet history: Tim Berners-Lee WWW invention, DNS, HTTP/HTTPS protocols",
            "Artificial Intelligence: Alan Turing (Turing Test 1950), Machine Learning, Neural Networks",
            "Robotics: Actuators (movement producing muscles), Sensors, Asimov's Laws",
            "Cybersecurity: Types of attacks (Ransomware encryption extortion, Phishing, DDoS), CERT-In nodal agency",
            "Information Technology Act 2000 (Section 66A struck down in Shreya Singhal case 2015)",
            "E-Commerce & Digital Payments: Unified Payments Interface (UPI developed by NPCI), cloud models (IaaS, PaaS, SaaS)"
        ]
    },
    "Unit 10": {
        "title_en": "National and Regional Constitutional / Statutory Commissions",
        "title_hi": "राष्ट्रीय एवं प्रादेशिक संवैधानिक / सांविधिक संस्थाएं (आयोग)",
        "weightage": 10,
        "key_themes": [
            "Election Commission of India (Article 324, tenure 6 years or 65 years age)",
            "MP State Election Commission (Article 243K, first commissioner N.B. Lohani)",
            "Union and State Public Service Commissions: MPPSC (Section 118(3) States Reorganisation Act 1956)",
            "Comptroller and Auditor General of India (Article 148, tenure 6 years or 65 years)",
            "NITI Aayog (established 1 January 2015 via Cabinet resolution, PM Chairperson)",
            "National Human Rights Commission (NHRC Act 1993, 2019 amendment eligible Chairperson CJI or SC Judge)",
            "National Commission for Women (NCW Act 1990, first Chairperson Jayanti Patnaik)",
            "National Commissions for SC (Art 338), ST (Art 338A 89th Amendment 2003), OBC (Art 338B 102nd Amendment)",
            "Central Information Commission (RTI Act 2005, appointment committee: PM, LoP, Cabinet Minister)",
            "National Green Tribunal (NGT Act 2010, Principal Bench New Delhi, Central Zonal Bench at Bhopal)"
        ]
    }
}

# Real MPPSC Exam Question Types & Historical Distribution
QUESTION_STYLE_DISTRIBUTION = {
    "DIRECT_FACTUAL": 0.55,       # 55% direct concept/fact
    "MULTI_STATEMENT": 0.20,      # 20% Statement 1 & 2 "Which is correct?"
    "MATCH_LIST": 0.15,           # 15% Match List-I with List-II
    "CHRONOLOGY_ORDER": 0.05,     # 5% Chronological ordering / Assertion-Reason
    "NEGATIVE_SELECTION": 0.05    # 5% "Which of the following is NOT correct?"
}

# Exam-level Difficulty Spectrum
DIFFICULTY_TARGETS = {
    "EASY": 0.35,        # 35 questions (Standard MPPSC syllabus essentials)
    "MODERATE": 0.50,    # 50 questions (In-depth factual and statutory nuances)
    "DIFFICULT": 0.15    # 15 questions (Analytical multi-statement & deeper distinctions)
}

def get_unit_details(unit_name: str) -> Dict[str, Any]:
    """Retrieve official syllabus details for a given unit."""
    return MPPSC_SYLLABUS_BLUEPRINT.get(unit_name, {})

def get_all_units() -> List[str]:
    """Return all 10 official units."""
    return list(MPPSC_SYLLABUS_BLUEPRINT.keys())
