from app.models.service_order import ServiceOrder
from app.models.service_order_item import ServiceOrderItem
from app.models.service_type import ServiceType

from app.repositories.service_order_repositoy import ServiceOrderRepository
from app.repositories.service_order_item_repository import ServiceOrderItemRepository
from app.repositories.service_type_repository import ServiceTypeRepository

from app.core.exceptions import ServiceTypeNotFoundError, ServiceTypeInactiveError

from sqlalchemy.orm import Session


class ServiceOrderService:

    def __init__(
        self,
        session: Session,
        service_order_repository: ServiceOrderRepository,
        service_order_item_repository: ServiceOrderItemRepository,
        service_type_repository: ServiceTypeRepository,
    ):
        
        self.session = session 
        self.service_order_repository = service_order_repository
        self.service_order_item_repository = service_order_item_repository
        self.service_type_repository = service_type_repository


    def validate_service_types(self, service_type_ids: list[int]):
        # Verifica se todos os IDs de tipos de serviço existem no banco de dados
        service_types = []

        for service_type_id in service_type_ids:
            service_type = self.service_type_repository.get_by_id(service_type_id)

            if service_type is None:
                raise ServiceTypeNotFoundError(f"Tipo de serviço com ID {service_type_id} não encontrado.")

            if not service_type.is_active:
                raise ServiceTypeInactiveError(f"Tipo de serviço com ID {service_type_id} está desativado.")

            service_types.append(service_type)

        return service_types

    def create_service_order(self, plate: str, employee_id: int, service_type_ids: list[int]) -> ServiceOrder:
        # Valida os tipos de serviço

        try:
            service_types = self.validate_service_types(service_type_ids) 

            service_order = ServiceOrder( plate = plate, employee_id = employee_id)

            self.service_order_repository.create(service_order)

            for service_type in service_types:
                service_order_item = ServiceOrderItem(
                    service_order_id = service_order.id,
                    service_type_id = service_type.id,
                )

                self.service_order_item_repository.create(service_order_item)

            self.session.commit()

            return service_order

        except Exception:
            self.session.rollback()
            raise