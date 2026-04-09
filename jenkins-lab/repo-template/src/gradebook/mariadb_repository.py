from __future__ import annotations

import os
from typing import Callable

import pymysql
from pymysql.cursors import DictCursor

from .domain import GradeRecord


ConnectionFactory = Callable[[], pymysql.connections.Connection]


class MariaDbGradeRepository:
    def __init__(self, connection_factory: ConnectionFactory | None = None) -> None:
        self._connection_factory = connection_factory or self._build_connection

    def _build_connection(self) -> pymysql.connections.Connection:
        return pymysql.connect(
            host=os.getenv('APP_DB_HOST', '127.0.0.1'),
            port=int(os.getenv('APP_DB_PORT', '3306')),
            user=os.getenv('APP_DB_USER', 'gradebook'),
            password=os.getenv('APP_DB_PASSWORD', 'gradebookpass'),
            database=os.getenv('APP_DB_NAME', 'gradebook'),
            cursorclass=DictCursor,
            autocommit=True,
        )

    def create_schema(self) -> None:
        with self._connection_factory() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS grades (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        student_name VARCHAR(120) NOT NULL,
                        module_name VARCHAR(120) NOT NULL,
                        score INT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    '''
                )

    def truncate(self) -> None:
        with self._connection_factory() as connection:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM grades')

    def add_grade(self, record: GradeRecord) -> None:
        with self._connection_factory() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO grades (student_name, module_name, score) VALUES (%s, %s, %s)',
                    (record.student_name, record.module_name, record.score),
                )

    def list_grades_for_student(self, student_name: str) -> list[GradeRecord]:
        with self._connection_factory() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT student_name, module_name, score FROM grades WHERE student_name = %s ORDER BY module_name',
                    (student_name,),
                )
                rows = cursor.fetchall()

        return [
            GradeRecord(
                student_name=row['student_name'],
                module_name=row['module_name'],
                score=int(row['score']),
            )
            for row in rows
        ]