# -*- coding: utf-8 -*-
"""
MPPSC Duplicate Detection & Controlled Revision Engine
Enforces strict uniqueness, semantic similarity analysis,
and intelligent candidate revision quotas (80-90% Unseen / 10-20% Revision).
"""

import re
import string
from typing import List, Dict, Tuple, Set, Any

STOPWORDS = {
    "what", "which", "who", "when", "where", "how", "why", "is", "are", "was",
    "were", "the", "a", "an", "in", "on", "at", "by", "for", "with", "about",
    "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there",
    "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "s", "t", "can", "will", "just", "don", "should", "now", "of",
    "and", "or", "as", "following", "called", "known", "situated", "located",
    "state", "district", "city", "year", "act", "article", "madhya", "pradesh",
    "निम्नलिखित", "में", "से", "कौन", "सा", "है", "था", "थी", "थे", "का", "के", "की"
}

def tokenize(text: str) -> Set[str]:
    """Normalize text and extract meaningful word tokens."""
    if not text:
        return set()
    # Remove punctuation
    text = text.lower()
    for ch in string.punctuation:
        text = text.replace(ch, " ")
    tokens = text.split()
    return {t for t in tokens if len(t) > 2 and t not in STOPWORDS}

def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Compute Jaccard similarity index between two token sets."""
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return intersection / union if union > 0 else 0.0

def are_exact_duplicates(q1: Dict[str, Any], q2: Dict[str, Any]) -> bool:
    """Check if two questions are character/text exact duplicates."""
    en1 = q1.get("question_en", "").strip().lower()
    en2 = q2.get("question_en", "").strip().lower()
    if en1 == en2 and len(en1) > 0:
        return True

    hi1 = q1.get("question_hi", "").strip().lower()
    hi2 = q2.get("question_hi", "").strip().lower()
    if hi1 == hi2 and len(hi1) > 0:
        return True

    return False

def are_semantic_duplicates(q1: Dict[str, Any], q2: Dict[str, Any], threshold: float = 0.72) -> Tuple[bool, float, str]:
    """
    Detect if two questions ask essentially the same concept
    through word variations or reordered options.
    """
    # 1. Exact match
    if are_exact_duplicates(q1, q2):
        return True, 1.0, "Exact question text match"

    tokens1_en = tokenize(q1.get("question_en", ""))
    tokens2_en = tokenize(q2.get("question_en", ""))
    sim_en = jaccard_similarity(tokens1_en, tokens2_en)

    tokens1_hi = tokenize(q1.get("question_hi", ""))
    tokens2_hi = tokenize(q2.get("question_hi", ""))
    sim_hi = jaccard_similarity(tokens1_hi, tokens2_hi)

    max_sim = max(sim_en, sim_hi)

    # 2. Check options overlap
    opts1 = {o.strip().lower() for o in q1.get("options_en", [])}
    opts2 = {o.strip().lower() for o in q2.get("options_en", [])}
    options_overlap = len(opts1.intersection(opts2))

    # If 3 or 4 options are identical and question similarity > 0.45
    if options_overlap >= 3 and max_sim > 0.45:
        return True, max_sim, f"High semantic similarity ({max_sim:.2f}) with identical options overlap ({options_overlap}/4)"

    # If pure question text similarity is above threshold
    if max_sim >= threshold:
        return True, max_sim, f"Semantic duplicate threshold exceeded ({max_sim:.2f} >= {threshold})"

    return False, max_sim, "Unique question"

class TestAssembler:
    """
    Assembles a 100-question mock test applying:
    1. Zero duplicate policy within the test.
    2. Controlled revision ratio (default: 85% unseen, 15% revision).
    3. Weak-area prioritization for revision slots.
    """
    def __init__(self, question_bank, unseen_ratio: float = 0.85, revision_ratio: float = 0.15):
        self.bank = question_bank
        self.unseen_ratio = unseen_ratio
        self.revision_ratio = revision_ratio

    def assemble_test(self, test_number: int = 1) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        total_required = 100
        target_revision = int(total_required * self.revision_ratio) if test_number > 1 else 0
        target_unseen = total_required - target_revision

        all_questions = self.bank.get_all()

        # Partition into unseen and seen
        unseen_pool = [q for q in all_questions if q.get("stats", {}).get("times_served", 0) == 0]
        seen_pool = [q for q in all_questions if q.get("stats", {}).get("times_served", 0) > 0]

        # Prioritize weak questions in seen pool
        weak_pool = [q for q in seen_pool if q.get("stats", {}).get("times_incorrect", 0) > 0 or q.get("stats", {}).get("times_unattempted", 0) > 0]
        other_seen = [q for q in seen_pool if q not in weak_pool]

        selected_questions: List[Dict[str, Any]] = []
        selected_ids: Set[str] = set()

        # 1. Select revision questions (prioritizing weak areas)
        revision_selected = 0
        for pool in [weak_pool, other_seen]:
            for q in pool:
                if revision_selected >= target_revision:
                    break
                if q["id"] not in selected_ids:
                    # Duplicate check against already selected
                    is_dup = False
                    for existing in selected_questions:
                        dup, _, _ = are_semantic_duplicates(existing, q)
                        if dup:
                            is_dup = True
                            break
                    if not is_dup:
                        selected_questions.append(q)
                        selected_ids.add(q["id"])
                        revision_selected += 1

        # 2. Select unseen questions
        unseen_selected = 0
        for q in unseen_pool:
            if len(selected_questions) >= total_required:
                break
            if q["id"] not in selected_ids:
                is_dup = False
                for existing in selected_questions:
                    dup, _, _ = are_semantic_duplicates(existing, q)
                    if dup:
                        is_dup = True
                        break
                if not is_dup:
                    selected_questions.append(q)
                    selected_ids.add(q["id"])
                    unseen_selected += 1

        # 3. If bank had insufficient unseen, fill from remaining seen pool
        if len(selected_questions) < total_required:
            for q in all_questions:
                if len(selected_questions) >= total_required:
                    break
                if q["id"] not in selected_ids:
                    is_dup = False
                    for existing in selected_questions:
                        dup, _, _ = are_semantic_duplicates(existing, q)
                        if dup:
                            is_dup = True
                            break
                    if not is_dup:
                        selected_questions.append(q)
                        selected_ids.add(q["id"])

        metadata = {
            "test_number": test_number,
            "total_questions": len(selected_questions),
            "unseen_count": unseen_selected,
            "revision_count": revision_selected,
            "unseen_ratio_achieved": f"{(unseen_selected / len(selected_questions) * 100):.1f}%" if selected_questions else "0%",
            "revision_ratio_achieved": f"{(revision_selected / len(selected_questions) * 100):.1f}%" if selected_questions else "0%",
            "bank_size": len(all_questions)
        }

        return selected_questions, metadata
