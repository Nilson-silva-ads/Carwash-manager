from datetime import datetime

from sqlalchemy import func, select, extract
from sqlalchemy.orm import Session

from app.models.service_order import ServiceOrder
from app.models.service_order_item import ServiceOrderItem
from app.models.service_type import ServiceType


class ReportRepository:
    
    def __init__(self, session: Session):
        self.session = session

    
    def count_service_orders( self, start_date: datetime, end_date: datetime) -> int:

        stmt = (
            select(func.count(ServiceOrder.id))
            .where(
                ServiceOrder.created_at >= start_date,
                ServiceOrder.created_at <= end_date,
            )
        )

        result = self.session.execute(stmt)

        return result.scalar_one()

    
    def count_services_by_type( self, start_date: datetime, end_date: datetime ):

        stmt = (
            select(
                ServiceType.id,
                ServiceType.name,
                func.count(ServiceOrderItem.id),
            )
            .join(
                ServiceOrderItem,
                ServiceOrderItem.service_type_id == ServiceType.id,
            )
            .join(
                ServiceOrder,
                ServiceOrder.id == ServiceOrderItem.service_order_id,
            )
            .where(
                ServiceOrder.created_at >= start_date,
                ServiceOrder.created_at <= end_date,
            )
            .group_by(
                ServiceType.id,
                ServiceType.name,
            )
            .order_by(
                ServiceType.id
            )
        )

        result = self.session.execute(stmt)

        return result.all()


    def count_service_orders_by_month( self, year: int):

        stmt = (
            select(
                extract("month", ServiceOrder.created_at),
                func.count(ServiceOrder.id),
            )
            .where(
                extract("year", ServiceOrder.created_at) == year
            )
            .group_by(
                extract("month", ServiceOrder.created_at)
            )
            .order_by(
                extract("month", ServiceOrder.created_at)
            )
        )

        result = self.session.execute(stmt)

        return result.all()