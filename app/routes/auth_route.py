from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.services.employee_service import EmployeeService
from app.schemas.auth_schema import LoginSchema, TokenSchema
from app.core.security import create_access_token

from app.dependencies.employee_dependencies import get_employee_service, get_current_employee

from app.models.employee import Employee



router = APIRouter(prefix="/employees", tags=["Employees"])



@router.post(
    "/login",
    response_model=TokenSchema,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: EmployeeService = Depends(get_employee_service),
):
    employee = service.authenticate_employee(
        username=form_data.username,
        password=form_data.password,
    )

    token = create_access_token(
        data={
            "sub": str(employee.id),
            "username": employee.username,
        }
    )

    return TokenSchema(
        token_type="bearer",
        access_token=token,
    )