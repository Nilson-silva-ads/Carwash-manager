from sqlalchemy.orm import Session

from fastapi import Depends

from app.database.session import get_db
from app.repositories.service_order_repository import ServiceOrderRepository
from app.repositories.service_order_item_repository import ServiceOrderItemRepository
from app.repositories.service_type_repository import ServiceTypeRepository
from app.services.service_order_service import ServiceOrderService


def get_service_order_service(
    db: Session = Depends(get_db),
) -> ServiceOrderService:

    service_order_repository = ServiceOrderRepository(db)
    service_order_item_repository = ServiceOrderItemRepository(db)
    service_type_repository = ServiceTypeRepository(db)

    return ServiceOrderService(
        session=db,
        service_order_repository=service_order_repository,
        service_order_item_repository=service_order_item_repository,
        service_type_repository=service_type_repository,
    )