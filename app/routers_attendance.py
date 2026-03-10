from typing import List

from fastapi import APIRouter

from .schemas import Attendance, AttendanceCreate, AttendanceSummary
from . import services_attendance as attendance_service


router = APIRouter(
    prefix="/employees/{employee_id}/attendance",
    tags=["attendance"],
)


@router.post("", response_model=Attendance, status_code=201)
def mark_attendance(employee_id: str, record: AttendanceCreate) -> Attendance:
    return attendance_service.mark_attendance(employee_id, record)


@router.get("", response_model=List[Attendance])
def get_attendance(employee_id: str) -> List[Attendance]:
    return attendance_service.get_attendance(employee_id)


@router.get("/summary", response_model=AttendanceSummary)
def get_attendance_summary(employee_id: str) -> AttendanceSummary:
    return attendance_service.get_attendance_summary(employee_id)

