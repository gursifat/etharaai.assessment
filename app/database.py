from __future__ import annotations

import sqlite3
from typing import Generator

from .config import settings


def get_connection() -> sqlite3.Connection:
    """
    Create a connection to the SQLite database.

    The actual file path comes from configuration (settings.db_path),
    so we can easily point to a different file in tests or production.
    """
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables() -> None:
    """
    Create the `employees` and `attendance` tables if they do not exist.

    This keeps all schema-related SQL in one place.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            day TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('Present', 'Absent')),
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        );
        """
    )

    conn.commit()
    conn.close()

