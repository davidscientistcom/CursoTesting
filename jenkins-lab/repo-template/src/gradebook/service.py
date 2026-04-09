from __future__ import annotations

from .domain import GradeRecord
from .repository import GradeRepository


class GradebookService:
    def __init__(self, repository: GradeRepository) -> None:
        self._repository = repository

    def register_grade(self, student_name: str, module_name: str, score: int) -> GradeRecord:
        if not student_name.strip():
            raise ValueError('student_name no puede estar vacio')
        if not module_name.strip():
            raise ValueError('module_name no puede estar vacio')
        if score < 0 or score > 100:
            raise ValueError('score debe estar entre 0 y 100')

        record = GradeRecord(
            student_name=student_name.strip(),
            module_name=module_name.strip(),
            score=score,
        )
        self._repository.add_grade(record)
        return record

    def average_for_student(self, student_name: str) -> float:
        records = self._repository.list_grades_for_student(student_name.strip())
        if not records:
            return 0.0
        return round(sum(record.score for record in records) / len(records), 2)