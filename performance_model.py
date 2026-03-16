"""Performance model and prediction utilities.

This module provides a simple, interpretable classifier that grades students as:
- Weak student (marks < 50)
- Average student (50 <= marks <= 75)
- Top student (marks > 75)

It also includes a scikit-learn pipeline stub for demonstration purposes.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.tree import DecisionTreeClassifier


def classify_mark(mark: float) -> str:
    """Classify a single mark into a performance bucket."""

    if mark < 50:
        return "Weak"
    if mark <= 75:
        return "Average"
    return "Top"


class RuleBasedPerformanceClassifier(BaseEstimator, ClassifierMixin):
    """A scikit-learn compatible classifier that uses rule-based logic."""

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        X_arr = np.array(X).flatten().astype(float)
        return [classify_mark(float(x)) for x in X_arr]


def build_pipeline() -> Pipeline:
    """Build a simple pipeline that can be used for scikit-learn style workflows."""

    pipeline = Pipeline([
        ("to_float", FunctionTransformer(lambda x: x.astype(float).reshape(-1, 1), validate=False)),
        ("classifier", RuleBasedPerformanceClassifier()),
    ])

    return pipeline


def annotate_student_performance(students: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Annotate each student record with a performance category per subject."""

    for student in students:
        subjects = student.get("subjects", [])
        marks = student.get("marks", [])
        categories: List[str] = []

        for mark in marks:
            categories.append(classify_mark(float(mark)))

        student["performance"] = categories

    return students


def get_overall_category(student: Dict[str, object]) -> str:
    """Return an overall category based on average marks."""

    marks = student.get("marks", [])
    if not marks:
        return "Unknown"

    avg = float(sum(marks) / len(marks))
    return classify_mark(avg)
