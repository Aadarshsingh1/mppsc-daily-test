# -*- coding: utf-8 -*-
"""
MPPSC Persistent Question Bank Engine
Maintains unique question IDs, rich syllabus metadata, PYQ attributions,
and candidate historical response telemetry.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

BANK_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "question_bank.json")

class QuestionBank:
    def __init__(self, storage_path: str = BANK_FILE):
        self.storage_path = storage_path
        self.questions: Dict[str, Dict[str, Any]] = {}
        self.load()

    def load(self) -> None:
        """Load questions from persistent JSON storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.questions = {q["id"]: q for q in data}
            except Exception as e:
                print(f"[Warning] Failed to load question bank from {self.storage_path}: {e}")
                self.questions = {}
        else:
            self.questions = {}

    def save(self) -> None:
        """Save question bank to persistent storage."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(list(self.questions.values()), f, ensure_ascii=False, indent=2)

    def add_question(self, q_data: Dict[str, Any]) -> str:
        """Add or update a question with validated metadata."""
        qid = q_data.get("id")
        if not qid:
            qid = f"MPPSC-Q-{len(self.questions) + 1:04d}"
            q_data["id"] = qid

        # Ensure default metadata fields
        defaults = {
            "unit": "Unit 1",
            "topic": "General",
            "subtopic": "General",
            "difficulty": "MODERATE",
            "question_type": "DIRECT_FACTUAL",
            "source_type": "ORIGINAL_PRACTICE",
            "pyq_metadata": None,
            "created_at": datetime.now().isoformat(),
            "stats": {
                "times_served": 0,
                "times_correct": 0,
                "times_incorrect": 0,
                "times_unattempted": 0,
                "last_served": None
            }
        }
        for k, v in defaults.items():
            if k not in q_data:
                q_data[k] = v

        self.questions[qid] = q_data
        return qid

    def get_question(self, qid: str) -> Optional[Dict[str, Any]]:
        return self.questions.get(qid)

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.questions.values())

    def total_count(self) -> int:
        return len(self.questions)

    def record_attempt(self, qid: str, outcome: str) -> None:
        """
        Record candidate interaction:
        outcome: 'CORRECT' | 'INCORRECT' | 'UNATTEMPTED'
        """
        if qid in self.questions:
            stats = self.questions[qid].setdefault("stats", {
                "times_served": 0,
                "times_correct": 0,
                "times_incorrect": 0,
                "times_unattempted": 0,
                "last_served": None
            })
            stats["times_served"] += 1
            stats["last_served"] = datetime.now().isoformat()
            if outcome == "CORRECT":
                stats["times_correct"] += 1
            elif outcome == "INCORRECT":
                stats["times_incorrect"] += 1
            elif outcome == "UNATTEMPTED":
                stats["times_unattempted"] += 1

    def get_weak_questions(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Retrieve questions that were previously incorrect or unattempted."""
        weak = []
        for q in self.questions.values():
            stats = q.get("stats", {})
            if stats.get("times_incorrect", 0) > 0 or stats.get("times_unattempted", 0) > 0:
                weak.append(q)
        # Sort by highest incorrect count
        weak.sort(key=lambda x: x.get("stats", {}).get("times_incorrect", 0), reverse=True)
        return weak[:limit]

    def get_unseen_questions(self) -> List[Dict[str, Any]]:
        """Retrieve questions that have never been served to the candidate."""
        return [q for q in self.questions.values() if q.get("stats", {}).get("times_served", 0) == 0]
