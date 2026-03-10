from datetime import date
from typing import List

from fastapi import HTTPException

from .database import get_connection
from .schemas import Attendance, AttendanceCreate, AttendanceSummary


def mark_attendance(employee_id: str, record: AttendanceCreate) -> Attendance:
    conn = get_connection()
    cursor = conn.cursor()

    # Check employee exists
    cursor.execute("SELECT 1 FROM employees WHERE employee_id = ?;", (employee_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Employee not found.")

    cursor.execute(
        """
        INSERT INTO attendance (employee_id, day, status)
        VALUES (?, ?, ?);
        """,
        (employee_id, record.day.isoformat(), record.status),
    )
    conn.commit()
    attendance_id = cursor.lastrowid

    cursor.execute(
        "SELECT id, employee_id, day, status FROM attendance WHERE id = ?;",
        (attendance_id,),
    )
    row = cursor.fetchone()
    conn.close()

    return Attendance(
        id=row["id"],
        employee_id=row["employee_id"],
        day=date.fromisoformat(row["day"]),
        status=row["status"],
    )


def get_attendance(employee_id: str) -> List[Attendance]:
    conn = get_connection()
    cursor = conn.cursor()

    # Ensure employee exists
    cursor.execute("SELECT 1 FROM employees WHERE employee_id = ?;", (employee_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Employee not found.")

    cursor.execute(
        """
        SELECT id, employee_id, day, status
        FROM attendance
        WHERE employee_id = ?
        ORDER BY day DESC;
        """,
        (employee_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        Attendance(
            id=row["id"],
            employee_id=row["employee_id"],
            day=date.fromisoformat(row["day"]),
            status=row["status"],
        )
        for row in rows
    ]


def get_attendance_summary(employee_id: str) -> AttendanceSummary:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT full_name FROM employees WHERE employee_id = ?;",
        (employee_id,),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Employee not found.")

    full_name = row["full_name"]

    cursor.execute(
        """
        SELECT
            SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present_days,
            SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS absent_days
        FROM attendance
        WHERE employee_id = ?;
        """,
        (employee_id,),
    )
    counts = cursor.fetchone()
    conn.close()

    present_days = counts["present_days"] or 0
    absent_days = counts["absent_days"] or 0

    return AttendanceSummary(
        employee_id=employee_id,
        full_name=full_name,
        total_present_days=present_days,
        total_absent_days=absent_days,
    )

