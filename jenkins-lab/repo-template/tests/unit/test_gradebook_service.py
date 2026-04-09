from __future__ import annotations

from gradebook.domain import GradeRecord
from gradebook.service import GradebookService


class FakeRepository:
    def __init__(self) -> None:
        self.records: list[GradeRecord] = []

    def add_grade(self, record: GradeRecord) -> None:
        self.records.append(record)

    def list_grades_for_student(self, student_name: str) -> list[GradeRecord]:
        return [record for record in self.records if record.student_name == student_name]


def test_register_grade_persists_record() -> None:
    repository = FakeRepository()
    service = GradebookService(repository)

    record = service.register_grade('Ada', 'matematicas', 18)

    assert record == GradeRecord(student_name='Ada', module_name='matematicas', score=18)
    assert repository.records == [record]


def test_average_for_student_uses_only_the_requested_student() -> None:
    repository = FakeRepository()
    service = GradebookService(repository)
    service.register_grade('Ada', 'matematicas', 18)
    service.register_grade('Ada', 'fisica', 16)
    service.register_grade('Linus', 'matematicas', 10)

    assert service.average_for_student('Ada') == 17.0


def test_average_returns_zero_when_student_has_no_records() -> None:
    repository = FakeRepository()
    service = GradebookService(repository)

    assert service.average_for_student('Grace') == 0.0


def test_register_grade_rejects_invalid_scores() -> None:
    repository = FakeRepository()
    service = GradebookService(repository)

    try:
        service.register_grade('Ada', 'matematicas', 120)
    except ValueError as error:
        assert 'score' in str(error)
    else:
        raise AssertionError('Se esperaba ValueError para una nota invalida')