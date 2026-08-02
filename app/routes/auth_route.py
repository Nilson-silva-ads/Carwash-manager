from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.employee_service import EmployeeService, get_current_employee
from app.schemas.auth_schema import LoginSchema, TokenSchema
from app.core.security import create_access_token
from app.dependencies.employee_dependencies import get_employee_service


router = APIRouter(prefix="/employees", tags=["Employees"])



@router.post(
    "/login",
    response_model=TokenSchema,
)
def login(
    login_data: LoginSchema,  #recebe os dados do login.
    service: EmployeeService = Depends(get_employee_service),  #chama o employeeService.
):
    employee = service.authenticate_employee(
        username=login_data.username,
        password=login_data.password,
    )

    token = create_access_token(
        data={
        "sub": str(employee.id),
        "username": employee.username,
        }
      )

    return TokenSchema(token_type="bearer", access_token=token)



@router.get("")
def get_employees(
    current_employee: Employee = Depends(get_current_employee),
    service: EmployeeService = Depends(get_employee_service),
):
    employees = service.get_all_employes()
    return employees