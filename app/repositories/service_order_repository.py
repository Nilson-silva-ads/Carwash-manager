from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from datetime import datetime

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


    def get_by_date_range( self, start_date: datetime, end_date: datetime ) -> list[ServiceOrder]:

        stmt = (
            select(self.model).where(
                self.model.created_at >= start_date,
                self.model.created_at <= end_date,
            ).order_by( desc(self.model.created_at) )
        )

        result = self.session.execute(stmt)

        return result.scalars().all()

    
    def get_filtered( self, plate: str | None=None, employee_id: int | None=None, start_date: datetime | None=None, end_date: datetime | None=None ) -> list[ServiceOrder]:

        stmt = select(self.model)

        if plate is not None:
            stmt = stmt.where(self.model.plate == plate)

        if employee_id is not None:
            stmt = stmt.where(self.model.employee_id == employee_id)

        if start_date is not None:
            stmt = stmt.where(self.model.created_at >= start_date)

        if end_date is not None:
            stmt = stmt.where(self.model.created_at <= end_date)

        stmt = stmt.order_by( desc(self.model.created_at) )

        result = self.session.execute(stmt)

        return result.scalars().all()