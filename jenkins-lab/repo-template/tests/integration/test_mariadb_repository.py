from __future__ import annotations

from gradebook.domain import GradeRecord
from gradebook.mariadb_repository import MariaDbGradeRepository
from gradebook.service import GradebookService


def test_repository_round_trip_against_real_mariadb() -> None:
    repository = MariaDbGradeRepository()
    repository.create_schema()
    repository.truncate()

    repository.add_grade(GradeRecord(student_name='Ada', module_name='matematicas', score=18))

    assert repository.list_grades_for_student('Ada') == [
        GradeRecord(student_name='Ada', module_name='matematicas', score=18)
    ]


def test_service_average_runs_against_real_mariadb() -> None:
    repository = MariaDbGradeRepository()
    repository.create_schema()
    repository.truncate()
    service = GradebookService(repository)

    service.register_grade('Ada', 'matematicas', 18)
    service.register_grade('Ada', 'fisica', 12)

    assert service.average_for_student('Ada') == 15.0