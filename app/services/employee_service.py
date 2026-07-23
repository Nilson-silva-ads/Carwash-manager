from app.repositories.employee_repository import EmployeeRepository
from app.models.employee import Employee
from app.core.security import hash_password, verify_password
from app.core.exceptions import EmployeeAlreadyExistsError, EmployeeInactiveError



class EmployeeService:

    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def create_employee(self, name: str, username: str, password: str) -> Employee:
        #Logica para criar um Funcionario.
       
        if self.employee_repository.get_by_username(username):
            raise ValueError(f"{username} já existe. Por favor, escolha outro.")

        employee = Employee(
            name=name,
            username=username,
            password_hash=hash_password(password)
        )

        return self.employee_repository.create(employee)

    def authenticate_employee(self, username: str, password: str) -> Employee:
            #Logica para autenticar um Funionario.
            employee = self.employee_repository.get_by_username(username)
    
            if employee is None:
                raise EmployeeAlreadyExistsError("Usuario ou senha invalidos.")
    
            if not verify_password(password, employee.password_hash):
                raise EmployeeAlreadyExistsError("Usuario ou senha invalidos.")
    
            if not employee.is_active:
                raise EmployeeInactiveError("Funcionario inativo")
    
            return employee

    def get_all_employees(self) -> list[Employee]:
        return self.employee_repository.get_all()

    

    def get_employee_by_id(self, employee_id: int) -> Employee:
        employee = self.employee_repository.get_by_id(employee_id)

        if employee is None:
            raise ValueError("Funcionario não encontrado.")

        return employee
    
    def update_employee(self, employee_id: int, name: str | None = None, username: str | None = None, password: str | None = None) -> Employee:
        employee = self.get_employee_by_id(employee_id)

        if name:
            employee.name = name
        if username:
            if self.employee_repository.get_by_username(username):
                raise ValueError(f"{username} já existe. Por favor, escolha outro.")
            employee.username = username
        if password:
            employee.password_hash = hash_password(password)

        return self.employee_repository.update(employee)
    
    def deactivate_employee(self, employee_id: int) -> Employee:
        employee = self.get_employee_by_id(employee_id)
        employee.is_active = False
        return self.employee_repository.update(employee)