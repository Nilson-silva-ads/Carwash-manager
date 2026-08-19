from sqlalchemy.orm import Session

from app.models.service_order_item import ServiceOrderItem

from app.repositories.base_repository import BaseRepository

class ServiceOrderItemRepository(BaseRepository[ServiceOrderItem]):
    def __init__(self, session: Session):
        super().__init__(session, ServiceOrderItem)