"""Syllabus management for AI-Based Personalized Learning System."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


class SyllabusManager:
    """Manage syllabus topics for subjects.

    Internally stores a mapping of { subject_name: [topic1, topic2, ...] }.
    """

    def __init__(self, initial_data: Optional[Dict[str, List[str]]] = None):
        self._syllabus: Dict[str, List[str]] = initial_data or {}

    def add_topic(self, subject: str, topic: str) -> None:
        """Add a topic to a subject syllabus."""

        subject_key = subject.strip()
        if not subject_key:
            return

        self._syllabus.setdefault(subject_key, [])
        if topic.strip() and topic not in self._syllabus[subject_key]:
            self._syllabus[subject_key].append(topic.strip())

    def get_topics(self, subject: str) -> List[str]:
        """Get topics for a subject."""

        return list(self._syllabus.get(subject, []))

    def get_all(self) -> Dict[str, List[str]]:
        """Get the entire syllabus mapping."""

        return {k: list(v) for k, v in self._syllabus.items()}

    def to_json(self, path: str) -> None:
        """Persist the syllabus mapping to a JSON file."""

        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        with path_obj.open("w", encoding="utf-8") as f:
            json.dump(self._syllabus, f, indent=2)

    @classmethod
    def load(cls, path: str) -> "SyllabusManager":
        """Load syllabus mapping from a JSON file."""

        path_obj = Path(path)
        if not path_obj.exists():
            return cls()

        with path_obj.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            return cls(initial_data={k: list(v) for k, v in data.items()})

        raise ValueError("Expected a dictionary in the syllabus JSON file.")
