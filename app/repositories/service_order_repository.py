from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models.service_order import ServiceOrder
from app.repositories.base_repository import BaseRepository

class ServiceOrderRepository(BaseRepository[ServiceOrder]):
    def __init__(self, session: Session):
        super().__init__(session, ServiceOrder)


    def get_by_plate(self, plate: str) -> list[ServiceOrder]:
        stmt = select(self.model).where(self.model.plate == plate).order_by(desc(self.model.created_at)
        )

        result = self.session.execute(stmt)

        return result.scalars().all()


    def get_by_employee_id(self, employee_id: int) -> list[ServiceOrder]:
        stmt = (
            select(self.model).where(self.model.employee_id == employee_id).order_by(desc(self.model.created_at))
        )

        result = self.session.execute(stmt)

        return result.scalars().all()