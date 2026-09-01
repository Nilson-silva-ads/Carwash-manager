class EmployeeInactiveError(Exception):
    """ Lança quando um funcionario inativo tenta acessar o sistema """
    pass

class EmployeeNotFoundError(Exception):
    """ Lança quando um funcionario não é encontrado no banco de dados """
    pass

class InvalidCredentialsError(Exception):
    """ Lança quando as credenciais são invalidas """
    pass

class ServiceTypeNotFoundError(Exception):
    """ Lança quando um tipo de serviço não é encontrado no banco de dados """
    pass

class ServiceTypeInactiveError(Exception):
    """ Lança quando um tipo de serviço está inativo """
    pass

class ServiceOrderWithoutServicesError(Exception):
    """ Lança quando um atendimento é criado sem serviços."""
    pass

class UsernameAlreadyExistsError(Exception):
    """ Lança erro quando o usuario não existir """
    pass

class ServiceTypeAlreadyExistsError(Exception):
    """ Lança erro quando tentar cadastrar o mesmo tipó de serviço """
    pass

class ServiceOrderNotFoundError(Exception):
    """ Lança erro quando um atendimento não é encontrado"""
    pass


class AdminRequiredError(Exception):
    """Lança quando um usuário sem permissão administrativa tenta acessar um recurso."""
    pass

class InvalidServiceCombinationError(Exception):
    """Lança quando serviços incompatíveis são combinados no mesmo carro."""
    pass
