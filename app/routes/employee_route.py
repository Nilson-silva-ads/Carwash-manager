from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.schemas.employee_schema import EmployeeCreateSchema, EmployeeResponseSchema

router = APIRouter(prefix="/employess", tags=["Employess"])

def get_employee_service(session: Session = Depends(get_db)) -> EmployeeService:  #antes de executar a funçao Session ele chama o get_db().
        
    repository = EmployeeRepository(session)  #Criamos o repositorio.
    service = EmployeeService(repository)  #Criamos o serviço.

    return service

   


@router.post("", response_model=EmployeeResponseSchema) #Usando o response_model=Em..., todas as respostas que vinher dessa rota sera um EmployeeResponseSchema.

def create_employee(
    employee_data: EmployeeCreateSchema,  #O employee_data recebe um schema.
    service: EmployeeService = Depends(get_employee_service)  #chama o service, o FastApo chama get_employee_service automaticamente e entrega um resultado para a variavel service.
    ):

    employee = service.create_employee(
        name=employee_data.name,
        username=employee_data.username,
        password=employee_data.password,
    )

    return EmployeeResponseSchema.model_validate(employee)