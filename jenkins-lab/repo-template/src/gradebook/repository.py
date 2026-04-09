from __future__ import annotations

from typing import Protocol

from .domain import GradeRecord


class GradeRepository(Protocol):
    def add_grade(self, record: GradeRecord) -> None:
        ...

    def list_grades_for_student(self, student_name: str) -> list[GradeRecord]:
        ...