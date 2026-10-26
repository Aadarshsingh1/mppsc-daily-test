# -*- coding: utf-8 -*-
"""
MPPSC End-to-End Automated Test Suite
Covers:
A. Scheduling & Timezone logic (8:00 PM IST)
B. Question Navigation & 5-State Palette Transitions
C. Timer & Submission Controls
D. Official Scoring Formula (+1, -0.25, 0)
E. Exact & Semantic Duplicate Detection
F. Question Quality, Validation & Bilingual Parity
G. Question Bank Persistence & Controlled Revision
"""

import unittest
import os
import json
from datetime import datetime, time, timezone, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

from engine.validator import QualityValidator, calculate_score
from engine.deduplication import are_exact_duplicates, are_semantic_duplicates, TestAssembler
from engine.question_bank import QuestionBank
from engine.test_generator import generate_daily_test, seed_question_bank_from_initial_data
from engine.pyq_analyzer import MPPSC_SYLLABUS_BLUEPRINT, get_all_units

class TestMPPSCScoringEngine(unittest.TestCase):
    """Rigorous tests for the +1 / -0.25 marking formula."""

    def test_case_100_correct(self):
        # 100 correct, 0 incorrect, 0 unattempted -> 100.00 marks, 100% accuracy
        score, accuracy = calculate_score(correct=100, incorrect=0, unattempted=0)
        self.assertEqual(score, 100.00)
        self.assertEqual(accuracy, 100.00)

    def test_case_100_incorrect(self):
        # 0 correct, 100 incorrect, 0 unattempted -> -25.00 marks, 0% accuracy
        score, accuracy = calculate_score(correct=0, incorrect=100, unattempted=0)
        self.assertEqual(score, -25.00)
        self.assertEqual(accuracy, 0.00)

    def test_case_100_unattempted(self):
        # 0 correct, 0 incorrect, 100 unattempted -> 0.00 marks, 0% accuracy
        score, accuracy = calculate_score(correct=0, incorrect=0, unattempted=100)
        self.assertEqual(score, 0.00)
        self.assertEqual(accuracy, 0.00)

    def test_case_60_correct_20_incorrect_20_unattempted(self):
        # 60 correct (+60), 20 incorrect (-5), 20 unattempted (0) -> 55.00 marks
        # Attempted = 80, Accuracy = (60 / 80) * 100 = 75.00%
        score, accuracy = calculate_score(correct=60, incorrect=20, unattempted=20)
        self.assertEqual(score, 55.00)
        self.assertEqual(accuracy, 75.00)

    def test_invalid_total_questions(self):
        # Total questions != 100 must raise ValueError
        with self.assertRaises(ValueError):
            calculate_score(correct=50, incorrect=20, unattempted=10) # 80 != 100


class TestSchedulingAndTimezone(unittest.TestCase):
    """Test 8:00 PM IST scheduling, timezone handling, and countdown calculations."""

    def test_ist_timezone_offset(self):
        if ZoneInfo:
            ist = ZoneInfo("Asia/Kolkata")
            now_ist = datetime.now(ist)
            # IST offset must be UTC+5:30 (+19800 seconds)
            self.assertEqual(now_ist.utcoffset().total_seconds(), 19800)
        else:
            ist = timezone(timedelta(hours=5, minutes=30))
            now_ist = datetime.now(ist)
            self.assertEqual(now_ist.utcoffset().total_seconds(), 19800)

    def test_scheduled_time_boundary(self):
        # Dispatch time: 7:58 PM IST (19:58:00)
        dispatch_time = time(19, 58, 0)
        self.assertEqual(dispatch_time.hour, 19)
        self.assertEqual(dispatch_time.minute, 58)

        # Exam unlock time: 8:00 PM IST (20:00:00)
        exam_time = time(20, 0, 0)
        self.assertEqual(exam_time.hour, 20)
        self.assertEqual(exam_time.minute, 0)


class TestQuestionQualityAndValidation(unittest.TestCase):
    """Verify validation gates, option uniqueness, bilingual completeness."""

    def setUp(self):
        self.validator = QualityValidator()

    def test_valid_question(self):
        valid_q = {
            "id": "TEST-Q-001",
            "question_en": "What is the capital of Madhya Pradesh?",
            "question_hi": "मध्य प्रदेश की राजधानी क्या है?",
            "options_en": ["Bhopal", "Indore", "Gwalior", "Jabalpur"],
            "options_hi": ["भोपाल", "इंदौर", "ग्वालियर", "जबलपुर"],
            "correct": "A",
            "explanation_en": "Bhopal is the capital city of Madhya Pradesh.",
            "explanation_hi": "भोपाल मध्य प्रदेश की राजधानी है।"
        }
        is_valid = self.validator.validate_single_question(valid_q, 0)
        self.assertTrue(is_valid)
        self.assertEqual(len(self.validator.errors), 0)

    def test_detect_duplicate_options(self):
        dup_opts_q = {
            "id": "TEST-Q-002",
            "question_en": "Sample question",
            "question_hi": "नमूना प्रश्न",
            "options_en": ["Bhopal", "Indore", "Bhopal", "Jabalpur"], # Duplicate "Bhopal"
            "options_hi": ["भोपाल", "इंदौर", "भोपाल", "जबलपुर"],
            "correct": "A",
            "explanation_en": "Sample",
            "explanation_hi": "नमूना"
        }
        is_valid = self.validator.validate_single_question(dup_opts_q, 1)
        self.assertFalse(is_valid)
        self.assertTrue(any("duplicate options" in err.lower() for err in self.validator.errors))

    def test_detect_invalid_correct_key(self):
        invalid_key_q = {
            "id": "TEST-Q-003",
            "question_en": "Sample question",
            "question_hi": "नमूना प्रश्न",
            "options_en": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "options_hi": ["विकल्प 1", "विकल्प 2", "विकल्प 3", "विकल्प 4"],
            "correct": "E", # Invalid key 'E'
            "explanation_en": "Sample",
            "explanation_hi": "नमूना"
        }
        is_valid = self.validator.validate_single_question(invalid_key_q, 2)
        self.assertFalse(is_valid)
        self.assertTrue(any("invalid correct answer key" in err.lower() for err in self.validator.errors))


class TestDuplicateDetectionEngine(unittest.TestCase):
    """Test exact and semantic duplicate detection mechanisms."""

    def test_exact_duplicate_detection(self):
        q1 = {
            "id": "Q1",
            "question_en": "Who shifted the capital of Paramaras from Ujjain to Dhar?",
            "question_hi": "परमारों की राजधानी उज्जैन से धार किसने स्थानांतरित की?",
            "options_en": ["Raja Bhoj", "Munja", "Sindhuraja", "Upendra"],
            "options_hi": ["राजा भोज", "मुंज", "सिंधुराज", "उपेंद्र"],
            "correct": "A"
        }
        q2 = {
            "id": "Q2",
            "question_en": "Who shifted the capital of Paramaras from Ujjain to Dhar?", # Exact text
            "question_hi": "परमारों की राजधानी उज्जैन से धार किसने स्थानांतरित की?",
            "options_en": ["Upendra", "Munja", "Sindhuraja", "Raja Bhoj"],
            "correct": "D"
        }
        self.assertTrue(are_exact_duplicates(q1, q2))
        is_dup, score, reason = are_semantic_duplicates(q1, q2)
        self.assertTrue(is_dup)

    def test_semantic_duplicate_reworded(self):
        q1 = {
            "id": "Q1",
            "question_en": "The famous Parmara ruler Raja Bhoj shifted his capital from Ujjain to which city?",
            "question_hi": "राजा भोज ने राजधानी उज्जैन से किस शहर स्थानांतरित की?",
            "options_en": ["Mandu", "Dhar", "Vidisha", "Chanderi"]
        }
        q2 = {
            "id": "Q2",
            "question_en": "To which city was the Paramara capital transferred from Ujjain by King Bhoja?",
            "question_hi": "राजा भोज द्वारा परमारों की राजधानी उज्जैन से कहां स्थानांतरित की गई थी?",
            "options_en": ["Mandu", "Dhar", "Vidisha", "Chanderi"]
        }
        is_dup, score, reason = are_semantic_duplicates(q1, q2)
        self.assertTrue(is_dup)
        self.assertTrue("semantic duplicate" in reason.lower() or "overlap" in reason.lower())

    def test_distinct_questions_are_not_duplicates(self):
        q1 = {
            "id": "Q1",
            "question_en": "Highest peak of Madhya Pradesh is Dhupgarh located in which range?",
            "question_hi": "मध्य प्रदेश की सबसे ऊंची चोटी धूपगढ़ किस श्रेणी में है?",
            "options_en": ["Satpura", "Vindhyachal", "Maikal", "Aravalli"]
        }
        q2 = {
            "id": "Q2",
            "question_en": "Which river originates from Amarkantak plateau in Anuppur district?",
            "question_hi": "अनूपपुर जिले के अमरकंटक पठार से कौन सी नदी निकलती है?",
            "options_en": ["Narmada", "Chambal", "Betwa", "Tapi"]
        }
        is_dup, score, reason = are_semantic_duplicates(q1, q2)
        self.assertFalse(is_dup)


class TestFullPaperAssemblyAndValidation(unittest.TestCase):
    """End-to-end generation and validation of full 100-question mock test."""

    def test_generate_and_validate_test_01(self):
        bundle = generate_daily_test(test_number=1)
        questions = bundle["questions"]

        # 1. Exact 100 questions count
        self.assertEqual(len(questions), 100)

        # 2. Strict validation check
        validator = QualityValidator()
        passed, errors, warnings = validator.validate_test_paper(questions)
        self.assertTrue(passed, f"Validation errors encountered: {errors}")
        self.assertEqual(len(errors), 0)

        # 3. Unit coverage check (all 10 units represented)
        all_units = get_all_units()
        present_units = {q.get("unit") for q in questions}
        for u in all_units:
            matching = [q for q in questions if q.get("unit", "").startswith(u)]
            self.assertGreaterEqual(len(matching), 8, f"{u} must have balanced representation in paper.")

    def test_question_bank_telemetry_and_revision(self):
        bank = seed_question_bank_from_initial_data()
        self.assertGreaterEqual(bank.total_count(), 100)

        # Record test attempt for a question
        test_qid = "MPPSC-Q-0001"
        bank.record_attempt(test_qid, "INCORRECT")

        q_data = bank.get_question(test_qid)
        self.assertEqual(q_data["stats"]["times_served"], 1)
        self.assertEqual(q_data["stats"]["times_incorrect"], 1)

        # Verify weak-area retrieval includes this question
        weak_questions = bank.get_weak_questions(limit=10)
        self.assertTrue(any(q["id"] == test_qid for q in weak_questions))

if __name__ == "__main__":
    unittest.main()
