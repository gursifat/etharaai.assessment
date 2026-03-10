from typing import List
from datetime import date
import sqlite3

from fastapi import HTTPException

from .database import get_connection
from .schemas import Employee, EmployeeCreate


def list_employees() -> List[Employee]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT employee_id, full_name, email, department "
        "FROM employees ORDER BY full_name;"
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        Employee(
            employee_id=row["employee_id"],
            full_name=row["full_name"],
            email=row["email"],
            department=row["department"],
        )
        for row in rows
    ]


def create_employee(employee: EmployeeCreate) -> Employee:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO employees (employee_id, full_name, email, department)
            VALUES (?, ?, ?, ?);
            """,
            (employee.employee_id, employee.full_name, employee.email, employee.department),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        # This usually means duplicate employee_id
        raise HTTPException(status_code=400, detail="Employee ID already exists.")

    conn.close()
    return Employee(**employee.dict())


def delete_employee(employee_id: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM attendance WHERE employee_id = ?;", (employee_id,))
    cursor.execute("DELETE FROM employees WHERE employee_id = ?;", (employee_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Employee not found.")

