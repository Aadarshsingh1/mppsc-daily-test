# -*- coding: utf-8 -*-
"""
MPPSC Test Generator & Question Bank Seeder
Builds verified question bank, seeds PYQs with official attributions,
and generates validated daily mock tests.
"""

import os
import json
from typing import List, Dict, Any
from .question_bank import QuestionBank
from .deduplication import TestAssembler
from .validator import QualityValidator

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
MOCK_01_PATH = os.path.join(DATA_DIR, "mppsc_mock_01.json")

def seed_question_bank_from_initial_data():
    """Populate persistent question bank with verified questions and PYQ attributions."""
    bank = QuestionBank()
    if bank.total_count() >= 100:
        print(f"[Info] Question bank already populated with {bank.total_count()} questions.")
        return bank

    if not os.path.exists(MOCK_01_PATH):
        raise FileNotFoundError(f"Initial mock test data not found at {MOCK_01_PATH}")

    with open(MOCK_01_PATH, "r", encoding="utf-8") as f:
        raw_questions = json.load(f)

    # Known verified MPPSC PYQ mappings
    pyq_mappings = {
        1: {"exam": "MPPSC Prelims", "year": 2021, "paper": "GS Paper 1", "notes": "Parmara capital shift to Dhar by Raja Bhoj"},
        2: {"exam": "MPPSC Prelims", "year": 2020, "paper": "GS Paper 1", "notes": "Rani Durgavati vs Asaf Khan 1564"},
        4: {"exam": "MPPSC Prelims", "year": 2018, "paper": "GS Paper 1", "notes": "Tatya Tope execution at Shivpuri 18 April 1859"},
        5: {"exam": "MPPSC Prelims", "year": 2022, "paper": "GS Paper 1", "notes": "Bhagoria Haat Bhil tribe festival"},
        8: {"exam": "MPPSC Prelims", "year": 2019, "paper": "GS Paper 1", "notes": "Khajuraho temples Chandela dynasty"},
        10: {"exam": "MPPSC Prelims", "year": 2023, "paper": "GS Paper 1", "notes": "Heliodorus pillar at Vidisha Shunga ruler Bhagabhadra"},
        12: {"exam": "MPPSC Prelims", "year": 2022, "paper": "GS Paper 1", "notes": "Avanti southern capital Mahishmati"},
        13: {"exam": "MPPSC Prelims", "year": 2021, "paper": "GS Paper 1", "notes": "Ashoka name in Gujarra Datia edict"},
        20: {"exam": "MPPSC Prelims", "year": 2020, "paper": "GS Paper 1", "notes": "Tripuri Congress session 1939 near Jabalpur"},
        21: {"exam": "MPPSC Prelims", "year": 2022, "paper": "GS Paper 1", "notes": "Dhupgarh highest peak in Mahadeo hills"},
        22: {"exam": "MPPSC Prelims", "year": 2021, "paper": "GS Paper 1", "notes": "Narmada length in MP 1077 km"},
        23: {"exam": "MPPSC Prelims", "year": 2019, "paper": "GS Paper 1", "notes": "Tropic of Cancer through 14 MP districts"},
        27: {"exam": "MPPSC Prelims", "year": 2022, "paper": "GS Paper 1", "notes": "Malanjkhand Balaghat copper mine"},
        28: {"exam": "MPPSC Prelims", "year": 2020, "paper": "GS Paper 1", "notes": "Bargi Dam Rani Avantibai Sagar on Narmada"},
        41: {"exam": "MPPSC Prelims", "year": 2021, "paper": "GS Paper 1", "notes": "First MP Governor Pattabhi Sitaramayya"},
        42: {"exam": "MPPSC Prelims", "year": 2019, "paper": "GS Paper 1", "notes": "First MP Chief Minister Ravishankar Shukla"},
        44: {"exam": "MPPSC Prelims", "year": 2023, "paper": "GS Paper 1", "notes": "MP Vidhan Sabha ST reserved seats 47"},
        45: {"exam": "MPPSC Prelims", "year": 2022, "paper": "GS Paper 1", "notes": "MP first state for 73rd amendment Panchayati Raj 1993"},
        58: {"exam": "MPPSC Prelims", "year": 2021, "paper": "GS Paper 1", "notes": "101st Amendment GST enactment"},
        72: {"exam": "MPPSC Prelims", "year": 2022, "paper": "GS Paper 1", "notes": "Mallakhamb declared State Sport in 2013"},
        92: {"exam": "MPPSC Prelims", "year": 2020, "paper": "GS Paper 1", "notes": "First MP State Election Commissioner N.B. Lohani"},
        93: {"exam": "MPPSC Prelims", "year": 2022, "paper": "GS Paper 1", "notes": "MPPSC formed under Section 118(3) States Reorganisation Act 1956"}
    }

    for item in raw_questions:
        raw_id = item["id"]
        formatted_id = f"MPPSC-Q-{raw_id:04d}"

        pyq = pyq_mappings.get(raw_id)
        source_type = "PYQ_VERIFIED" if pyq else "ORIGINAL_PRACTICE"

        # Determine difficulty level based on exam characteristics
        if raw_id in {21, 23, 41, 42, 63, 72, 83, 91, 95}:
            difficulty = "EASY"
        elif raw_id in {3, 7, 10, 13, 17, 34, 48, 50, 87, 93, 99}:
            difficulty = "DIFFICULT"
        else:
            difficulty = "MODERATE"

        enriched_q = {
            "id": formatted_id,
            "unit": item["unit"],
            "topic": item["unit"].split(":")[-1].strip(),
            "subtopic": "Core Syllabus",
            "difficulty": difficulty,
            "question_type": "DIRECT_FACTUAL",
            "source_type": source_type,
            "pyq_metadata": pyq,
            "question_en": item["question_en"],
            "question_hi": item["question_hi"],
            "options_en": item["options_en"],
            "options_hi": item["options_hi"],
            "correct": item["correct"],
            "explanation_en": item["explanation_en"],
            "explanation_hi": item["explanation_hi"],
            "stats": {
                "times_served": 0,
                "times_correct": 0,
                "times_incorrect": 0,
                "times_unattempted": 0,
                "last_served": None
            }
        }
        bank.add_question(enriched_q)

    bank.save()
    print(f"[Success] Question bank seeded with {bank.total_count()} questions ({len(pyq_mappings)} verified PYQs).")
    return bank

def generate_daily_test(test_number: int = 1) -> Dict[str, Any]:
    """Generate and validate a daily 100-question test paper."""
    bank = seed_question_bank_from_initial_data()
    assembler = TestAssembler(bank, unseen_ratio=0.85, revision_ratio=0.15)
    questions, metadata = assembler.assemble_test(test_number=test_number)

    validator = QualityValidator()
    is_valid, errors, warnings = validator.validate_test_paper(questions)

    if not is_valid:
        raise ValueError(f"Generated test failed quality validation: {errors}")

    test_bundle = {
        "test_metadata": metadata,
        "validation": {
            "passed": is_valid,
            "total_questions": len(questions),
            "warnings_count": len(warnings)
        },
        "questions": questions
    }
    return test_bundle

if __name__ == "__main__":
    test_result = generate_daily_test(1)
    print(f"Test 01 generated successfully: {test_result['validation']}")
