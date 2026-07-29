from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.schemas.employee_schema import EmployeeCreateSchema, EmployeeResponseSchema, EmployeeUpdateSchema

router = APIRouter(prefix="/employees", tags=["Employees"])

def get_employee_service(session: Session = Depends(get_db)) -> EmployeeService:  #antes de executar a funçao Session ele chama o get_db().
        
    repository = EmployeeRepository(session)  #Criamos o repositorio.
    service = EmployeeService(repository)  #Criamos o serviço.

    return service

   


@router.post("", response_model=EmployeeResponseSchema) #Usando o response_model=Em..., todas as respostas que vinher dessa rota sera um EmployeeResponseSchema.

def create_employee(
    employee_data: EmployeeCreateSchema,  #O employee_data recebe um schema.
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
        service: EmployeeService = Depends(get_employee_service)
):
    employee = service.get_employee_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Funcionario não encontrado.",
            )

    return EmployeeResponseSchema.model_validate(employee)


@router.put(
        "/{employee_id}",
        response_model=EmployeeResponseSchema,
    )

def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdateSchema,
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
    service: EmployeeService = Depends(get_employee_service)
):
    employee = service.deactivate_employee(employee_id)
    return EmployeeResponseSchema.model_validate(employee)