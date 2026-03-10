from typing import List

from fastapi import APIRouter

from .schemas import Employee, EmployeeCreate
from . import services_employees as employee_service


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=List[Employee])
def list_employees() -> List[Employee]:
    return employee_service.list_employees()


@router.post("", response_model=Employee, status_code=201)
def add_employee(employee: EmployeeCreate) -> Employee:
    return employee_service.create_employee(employee)


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: str) -> None:
    employee_service.delete_employee(employee_id)

