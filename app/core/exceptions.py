class EmployeeAlreadyExistsError(Exception):
    """ Lança quando ja existe um funcionario com o mesmo username """

class AuthenticationError(Exception):
    """ Lança quando as credenciais são invalidas """

class EmployeeInactiveError(Exception):
    """ Lança quando um funcionario inativo tenta acessar o sistema """