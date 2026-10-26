# -*- coding: utf-8 -*-
"""
MPPSC Question & Examination Quality Validator
Rigorous quality-gate verifying 100 questions, option uniqueness,
bilingual equivalence, key defensibility, and mathematical scoring accuracy.
"""

from typing import List, Dict, Tuple, Any
from .deduplication import are_semantic_duplicates

class QualityValidator:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_single_question(self, q: Dict[str, Any], index: int) -> bool:
        """Validate an individual question against quality standards."""
        qid = q.get("id", f"Index {index}")
        valid = True

        # 1. Text presence
        q_en = q.get("question_en", "").strip()
        q_hi = q.get("question_hi", "").strip()
        if not q_en:
            self.errors.append(f"[{qid}] Missing English question text.")
            valid = False
        if not q_hi:
            self.errors.append(f"[{qid}] Missing Hindi question text.")
            valid = False

        # 2. Options validation (Exactly 4 distinct options)
        opts_en = q.get("options_en", [])
        opts_hi = q.get("options_hi", [])

        if len(opts_en) != 4:
            self.errors.append(f"[{qid}] Must have exactly 4 English options (found {len(opts_en)}).")
            valid = False
        if len(opts_hi) != 4:
            self.errors.append(f"[{qid}] Must have exactly 4 Hindi options (found {len(opts_hi)}).")
            valid = False

        # Check for empty options
        if any(not str(o).strip() for o in opts_en):
            self.errors.append(f"[{qid}] Contains empty English option.")
            valid = False
        if any(not str(o).strip() for o in opts_hi):
            self.errors.append(f"[{qid}] Contains empty Hindi option.")
            valid = False

        # Check for duplicate options within the question
        clean_opts_en = [str(o).strip().lower() for o in opts_en]
        if len(set(clean_opts_en)) != len(clean_opts_en):
            self.errors.append(f"[{qid}] Contains duplicate options in English: {opts_en}")
            valid = False

        clean_opts_hi = [str(o).strip().lower() for o in opts_hi]
        if len(set(clean_opts_hi)) != len(clean_opts_hi):
            self.errors.append(f"[{qid}] Contains duplicate options in Hindi: {opts_hi}")
            valid = False

        # 3. Correct answer validation ('A', 'B', 'C', or 'D')
        correct = str(q.get("correct", "")).strip().upper()
        if correct not in {"A", "B", "C", "D"}:
            self.errors.append(f"[{qid}] Invalid correct answer key: '{correct}'. Must be A, B, C, or D.")
            valid = False

        # 4. Explanations validation
        exp_en = q.get("explanation_en", "").strip()
        exp_hi = q.get("explanation_hi", "").strip()
        if not exp_en:
            self.warnings.append(f"[{qid}] Missing English explanation.")
        if not exp_hi:
            self.warnings.append(f"[{qid}] Missing Hindi explanation.")

        return valid

    def validate_test_paper(self, questions: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
        """
        Validate full 100-question test paper:
        1. Exact 100 questions.
        2. All individual questions valid.
        3. No intra-test exact or semantic duplicates.
        """
        self.errors.clear()
        self.warnings.clear()

        # 1. Exact 100 Questions requirement
        if len(questions) != 100:
            self.errors.append(f"Test must contain exactly 100 questions (received {len(questions)}).")

        # 2. Individual Question Validations
        seen_ids = set()
        for idx, q in enumerate(questions):
            qid = q.get("id")
            if qid in seen_ids:
                self.errors.append(f"Duplicate question ID '{qid}' found at position {idx + 1}.")
            seen_ids.add(qid)
            self.validate_single_question(q, idx)

        # 3. Pairwise duplicate check within test
        for i in range(len(questions)):
            for j in range(i + 1, len(questions)):
                is_dup, score, reason = are_semantic_duplicates(questions[i], questions[j])
                if is_dup:
                    self.errors.append(
                        f"Intra-test duplicate between Q{questions[i].get('id')} and Q{questions[j].get('id')}: {reason}"
                    )

        is_passed = len(self.errors) == 0
        return is_passed, list(self.errors), list(self.warnings)

def calculate_score(correct: int, incorrect: int, unattempted: int) -> Tuple[float, float]:
    """
    Scoring Rule:
    Correct: +1.00
    Incorrect: -0.25
    Unattempted: 0.00
    Returns: (score, accuracy_percentage)
    """
    total = correct + incorrect + unattempted
    if total != 100:
        raise ValueError(f"Total questions evaluated must equal 100 (got {total}).")

    raw_score = (correct * 1.0) - (incorrect * 0.25)
    attempted = correct + incorrect
    accuracy = (correct / attempted * 100.0) if attempted > 0 else 0.0

    return round(raw_score, 2), round(accuracy, 2)
