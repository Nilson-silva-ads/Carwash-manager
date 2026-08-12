from sqlalchemy.orm import Session

from app.models.service_order import ServiceOrder
from app.repositories.base_repository import BaseRepository

class ServiceOrderRepository(BaseRepository[ServiceOrder]):
    def __init__(self, session: Session):
        super().__init__(session, ServiceOrder)