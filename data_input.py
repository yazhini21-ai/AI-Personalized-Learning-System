"""Data input utilities for AI-Based Personalized Learning System.

This module provides helper functions to create and manage student performance
records (marks, attendance, study hours) in a tabular format.

The design is intentionally simple so it can be extended for real persistence
(e.g., databases) later.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


def create_student_record(
    name: str,
    subjects: List[str],
    marks: List[float],
    attendance: float,
    study_hours: float,
) -> Dict[str, Any]:
    """Create a student record dictionary from raw inputs."""

    if len(subjects) != len(marks):
        raise ValueError("The number of subjects must match the number of marks.")

    record = {
        "name": name.strip(),
        "attendance": float(attendance),
        "study_hours": float(study_hours),
        "subjects": subjects,
        "marks": [float(m) for m in marks],
    }

    return record


def students_to_dataframe(students: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert list of student records into a normalized pandas DataFrame."""

    rows: List[Dict[str, Any]] = []
    for student in students:
        name = student.get("name")
        attendance = student.get("attendance", 0.0)
        study_hours = student.get("study_hours", 0.0)
        subjects = student.get("subjects", [])
        marks = student.get("marks", [])

        for subject, mark in zip(subjects, marks):
            rows.append(
                {
                    "name": name,
                    "subject": subject,
                    "mark": float(mark),
                    "attendance": float(attendance),
                    "study_hours": float(study_hours),
                }
            )

    df = pd.DataFrame(rows)
    return df


def save_students(path: str, students: List[Dict[str, Any]]) -> None:
    """Persist students list to a JSON file."""

    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    with path_obj.open("w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)


def load_students(path: str) -> List[Dict[str, Any]]:
    """Load student records from a JSON file."""

    path_obj = Path(path)
    if not path_obj.exists():
        return []

    with path_obj.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

    raise ValueError("Expected a list of student records in the JSON file.")
