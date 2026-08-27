from fastapi import Depends, APIRouter

from app.services.employee_service import EmployeeService
from app.schemas.employee_schema import EmployeeCreateSchema, EmployeeResponseSchema, EmployeeUpdateSchema
from app.dependencies.employee_dependencies import get_employee_service, get_current_employee, get_current_admin
from app.models.employee import Employee


router = APIRouter(prefix="/employees", tags=["Employees"])




@router.post("", response_model=EmployeeResponseSchema) #Usando o response_model=Em..., todas as respostas que vinher dessa rota sera um EmployeeResponseSchema.

def create_employee(
    employee_data: EmployeeCreateSchema,  #O employee_data recebe um schema.
    current_admin: Employee = Depends(get_current_admin),  #chama o get_current_admin, o FastApi chama get_current_admin automaticamente e entrega um resultado para a variavel current_admin;
    service: EmployeeService = Depends(get_employee_service)  #chama o service, o FastApi chama get_employee_service automaticamente e entrega um resultado para a variavel service.
    ):

    employee = service.create_employee(
        name=employee_data.name,
        username=employee_data.username,
        password=employee_data.password,
    )

    return EmployeeResponseSchema.model_validate(employee)

@router.get(
    "",
     response_model=list[EmployeeResponseSchema],
     )

def get_employees(
    current_employee: Employee = Depends(get_current_employee), #chama o get_current_employee, o FastApi chama get_current_employee automaticamente e entrega um resultado para a variavel current_employee;
    service: EmployeeService = Depends(get_employee_service)  #chama o service, o FastApi chama get_employee_Service outomaticamente e entrega um resultado para a variavel service;   
):

    employees = service.get_all_employees()
    
    return [EmployeeResponseSchema.model_validate(employee)
             for employee in employees]

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponseSchema,
)

def get_employee_by_id(
        employee_id: int,
        current_employee: Employee = Depends(get_current_employee),
        service: EmployeeService = Depends(get_employee_service)
):
    employee = service.get_employee_by_id(employee_id)

   
    return EmployeeResponseSchema.model_validate(employee)


@router.put(
        "/{employee_id}",
        response_model=EmployeeResponseSchema,
    )

def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdateSchema,
    current_admin: Employee = Depends(get_current_admin),
    service: EmployeeService = Depends(get_employee_service)
):
    employee = service.update_employee(
        employee_id=employee_id,
        name=employee_data.name,
        username=employee_data.username
    )

    return EmployeeResponseSchema.model_validate(employee)


@router.patch(
    "/{employee_id}/deactivate",
    response_model=EmployeeResponseSchema,
)
def deactivate_employee(
    employee_id: int,
    current_admin: Employee = Depends(get_current_admin),
    service: EmployeeService = Depends(get_employee_service)
):
    employee = service.deactivate_employee(employee_id)
    return EmployeeResponseSchema.model_validate(employee)


@router.patch(
    "/{employee_id}/activate",
    response_model=EmployeeResponseSchema,
)
def activate_employee(
    employee_id: int,
    current_admin: Employee = Depends(get_current_admin),
    service: EmployeeService = Depends(get_employee_service),
):
    employee = service.activate_employee(employee_id)

    return EmployeeResponseSchema.model_validate(employee)