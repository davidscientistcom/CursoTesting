from __future__ import annotations

import os
import sys
import time

import pymysql


def main() -> int:
    deadline = time.time() + 60
    while time.time() < deadline:
        try:
            connection = pymysql.connect(
                host=os.getenv('APP_DB_HOST', '127.0.0.1'),
                port=int(os.getenv('APP_DB_PORT', '3306')),
                user=os.getenv('APP_DB_USER', 'gradebook'),
                password=os.getenv('APP_DB_PASSWORD', 'gradebookpass'),
                database=os.getenv('APP_DB_NAME', 'gradebook'),
                autocommit=True,
            )
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            connection.close()
            return 0
        except Exception:
            time.sleep(2)
    return 1


if __name__ == '__main__':
    sys.exit(main())