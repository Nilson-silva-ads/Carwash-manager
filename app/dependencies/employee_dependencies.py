from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.employee import Employee
from app.core.auth import oauth2_scheme
from app.core.security import decode_access_token
from app.core.exceptions import AdminRequiredError

from app.services.employee_service import EmployeeService
from app.repositories.employee_repository import EmployeeRepository


def get_employee_service(session: Session = Depends(get_db)) -> EmployeeService:  #antes de executar a funçao Session ele chama o get_db().
        
    repository = EmployeeRepository(session)  #Criamos o repositorio.
    service = EmployeeService(repository)  #Criamos o serviço.

    return service

def get_current_employee( 
        token: str = Depends(oauth2_scheme),
        service: EmployeeService = Depends(get_employee_service),
 ) -> Employee:

    payload = decode_access_token(token)
    employee = service.get_current_employee(payload)

    return employee


def get_current_admin(
        current_employee: Employee =  Depends(get_current_employee),
) -> Employee:

    if not current_employee.is_admin:
        raise AdminRequiredError(
           "Acesso permitido somente para administratores"
        )

    return current_employee