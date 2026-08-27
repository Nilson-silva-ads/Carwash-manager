from app.models.service_order import ServiceOrder
from app.models.service_order_item import ServiceOrderItem
from app.models.service_type import ServiceType

from app.repositories.service_order_repository import ServiceOrderRepository
from app.repositories.service_order_item_repository import ServiceOrderItemRepository
from app.repositories.service_type_repository import ServiceTypeRepository

from app.core.exceptions import ServiceTypeNotFoundError, ServiceTypeInactiveError, ServiceOrderWithoutServicesError, ServiceOrderNotFoundError
from sqlalchemy.orm import Session

from datetime import datetime


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


    def validate_service_types(self, service_type_ids: list[int]) -> list[ServiceType]:
        # Verifica se todos os IDs de tipos de serviço existem no banco de dados

        if not service_type_ids:
            raise ServiceOrderWithoutServicesError(f"O atendimento deve possuir pelo menos um serviço.")
        

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


        
            service_types = self.validate_service_types(service_type_ids) 

            service_order = ServiceOrder(
                plate=plate.strip().upper(),
                employee_id=employee_id,
            )

            self.service_order_repository.create(service_order)

            for service_type in service_types:
                service_order_item = ServiceOrderItem(
                    service_order_id = service_order.id,
                    service_type_id = service_type.id,
                )

                self.service_order_item_repository.create(service_order_item)

            return service_order




    def get_all_service_orders(self) -> list[ServiceOrder]:

        return self.service_order_repository.get_all()


    def get_service_order_by_id(self, service_order_id: int) -> ServiceOrder:

        
        service_order = self.service_order_repository.get_by_id(service_order_id)

        
        if service_order is None:
            raise ServiceOrderNotFoundError(f"Atendimento com Id {service_order_id} não encontrado.")

        return service_order

    
    def get_service_orders_by_plate(self, plate: str) -> list[ServiceOrder]:

        return self.service_order_repository.get_by_plate(plate.strip().upper())


    def get_service_orders_by_employee(self, employee_id: int) -> list[ServiceOrder]:

        return self.service_order_repository.get_by_employee_id(employee_id)

    def get_service_orders_by_date_range( self, start_date: datetime, end_date: datetime) -> list[ServiceOrder]:

        if start_date > end_date:
            raise ValueError( "A data inicial não pode ser maior que a data final." )

        return self.service_order_repository.get_by_date_range( start_date, end_date)


    def get_filtered_service_orders(
            self,
            plate: str | None=None,
            employee_id: int | None=None,
            start_date: datetime | None=None,
            end_date: datetime | None=None,
    ) -> list[ServiceOrder]:

        if start_date is not None and end_date is not None:
            if start_date > end_date:
                raise ValueError( "A data inicial não pode ser maior que a data final.")

        if plate is not None:
            plate = plate.strip().upper()

        return self.service_order_repository.get_filtered(
            plate=plate,
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
        )