from app.repositories.employee_repository import EmployeeRepository

from app.models.employee import Employee


from app.core.security import hash_password, verify_password
from app.core.exceptions import EmployeeInactiveError, EmployeeNotFoundError, UsernameAlreadyExistsError, InvalidCredentialsError



class EmployeeService:

    def __init__(
            self,
            employee_repository: EmployeeRepository,
    ):
        self.employee_repository = employee_repository

    def create_employee(self, name: str, username: str, password: str, is_admin: bool = False) -> Employee:
        #Logica para criar um Funcionario.
       
        if self.employee_repository.get_by_username(username):
            raise UsernameAlreadyExistsError(f"{username} já existe. Por favor, escolha outro.")

        employee = Employee(
            name=name,
            username=username,
            password_hash=hash_password(password),
            is_admin=is_admin,
        )

        return self.employee_repository.create(employee)
    

   
    def get_all_employees(self) -> list[Employee]:
        return self.employee_repository.get_all()

    

    def get_employee_by_id(self, employee_id: int) -> Employee:

        employee = self.employee_repository.get_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundError(
            f"Funcionário com ID {employee_id} não encontrado."
            )

        return employee

    
    def update_employee(self, employee_id: int, name: str | None = None, username: str | None = None) -> Employee:

        employee = self.get_employee_by_id(employee_id)

        if name is not None:
            employee.name = name  

        if username:
            existing_employee = self.employee_repository.get_by_username(username)

            if existing_employee and existing_employee.id != employee.id:
                raise UsernameAlreadyExistsError(f"Username '{username}' já existe.")

            employee.username = username
      
        return self.employee_repository.update(employee)


    
    def deactivate_employee(self, employee_id: int) -> Employee:

        employee = self.get_employee_by_id(employee_id)
        employee.is_active = False
        return self.employee_repository.update(employee)


    def activate_employee(self, employee_id: int) -> Employee:

        employee = self.get_employee_by_id(employee_id)

        employee.is_active = True

        return self.employee_repository.update(employee)


    def authenticate_employee(
        self, 
        username: str,
        password: str,
     ) -> Employee:
        
        employee = self.employee_repository.get_by_username(username)

        print("USERNAME", username)
        print("EMPLOYEE", employee)
        
        if employee is None:
            raise EmployeeNotFoundError("Usuario ou senha invalidos.")

        if not verify_password(password, employee.password_hash): 
            raise EmployeeNotFoundError("Usuario ou senha invalidos.") 

        if not employee.is_active:
            raise EmployeeInactiveError("Funcionario inativo.")
        
        return employee


    def get_current_employee(self, payload: dict) -> Employee:
        sub = payload.get("sub")

        if sub is None:
            raise InvalidCredentialsError("Token Inválido")

        employee_id = int(sub)

        employee = self.employee_repository.get_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundError("Funcionario não encontrado.")
        if not employee.is_active:
            raise EmployeeInactiveError("Funcionario inativo.")
        
        return employee