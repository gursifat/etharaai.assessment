from datetime import date
from typing import List

from pydantic import BaseModel, EmailStr, Field


# Employee schemas


class EmployeeBase(BaseModel):
    employee_id: str = Field(..., description="Unique employee ID, like EMP001")
    full_name: str
    email: EmailStr
    department: str


class EmployeeCreate(EmployeeBase):
    """Data needed when creating an employee."""

    pass


class Employee(EmployeeBase):
    """Data returned when reading an employee."""

    pass


# Attendance schemas


class AttendanceCreate(BaseModel):
    day: date
    # In Pydantic v2, use `pattern` instead of `regex`.
    status: str = Field(..., pattern="^(Present|Absent)$")


class Attendance(BaseModel):
    id: int
    employee_id: str
    day: date
    status: str


class AttendanceSummary(BaseModel):
    employee_id: str
    full_name: str
    total_present_days: int
    total_absent_days: int


# Convenience aliases for collections, mainly for type hints.

EmployeeList = List[Employee]
AttendanceList = List[Attendance]

