class EmployeeAlreadyExistsError(Exception):
    """ Lança quando ja existe um funcionario com o mesmo username """

class EmployeeInactiveError(Exception):
    """ Lança quando um funcionario inativo tenta acessar o sistema """

class EmployeeNotFoundError(Exception):
    """ Lança quando um funcionario não é encontrado no banco de dados """

class InvalidCredentialsError(Exception):
    """ Lança quando as credenciais são invalidas """