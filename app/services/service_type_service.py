from app.models.service_type import ServiceType
from app.core.exceptions import ServiceTypeAlreadyExistsError, ServiceTypeNotFoundError


class ServiceTypeService:
    def __init__(self, service_type_repository):
        self.service_type_repository = service_type_repository

    def get_service_type_by_name(self, name: str) -> ServiceType | None:
        return self.service_type_repository.get_by_name(name)
    
    def create_service_type(self, name: str) -> ServiceType | None:
        existing_service_type = self.get_service_type_by_name(name)

        if existing_service_type:
            raise ServiceTypeAlreadyExistsError("Tipo do Serviço já existe. Por favor, escolha outro.")

        new_service_type = ServiceType(name=name)
        self.service_type_repository.create(new_service_type)
        return new_service_type

    def get_all_service_types(self) -> list[ServiceType]:
        return self.service_type_repository.get_all()

    def get_service_type_by_id(self, service_type_id: int) -> ServiceType | None:
        return self.service_type_repository.get_by_id(service_type_id)

    def update_service_type(self, service_type_id: int, name: str) -> ServiceType | None:
        existing_service_type = self.get_service_type_by_id(service_type_id)

        if not existing_service_type:
            raise ServiceTypeNotFoundError("Tipo do Serviço não encontrado.")

        existing_service_type.name = name
        self.service_type_repository.update(existing_service_type)
        return existing_service_type

    def deactivate_service_type(self, service_type_id: int) -> ServiceType | None:
        existing_service_type = self.get_service_type_by_id(service_type_id)

        if not existing_service_type:
            raise ServiceTypeNotFoundError("Tipo do Serviço não encontrado.")

        existing_service_type.is_active = False
        self.service_type_repository.update(existing_service_type)
        return existing_service_type