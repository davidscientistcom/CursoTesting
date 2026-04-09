from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GradeRecord:
    student_name: str
    module_name: str
    score: int