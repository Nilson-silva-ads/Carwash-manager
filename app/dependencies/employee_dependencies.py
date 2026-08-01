from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.employee_service import EmployeeService
from app.database.session import get_db
from app.repositories.employee_repository import EmployeeRepository


def get_employee_service(session: Session = Depends(get_db)) -> EmployeeService:  #antes de executar a funçao Session ele chama o get_db().
        
    repository = EmployeeRepository(session)  #Criamos o repositorio.
    service = EmployeeService(repository)  #Criamos o serviço.

    return service