from datetime import datetime

from sqlalchemy import func, select, extract
from app.core.timezone import month_bounds_utc
from sqlalchemy.orm import Session

from app.models.service_order import ServiceOrder
from app.models.service_order_item import ServiceOrderItem
from app.models.service_type import ServiceType
from app.models.employee import Employee


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
        rows = []
        for month in range(1, 13):
            start, end = month_bounds_utc(year, month)
            total = self.session.execute(select(func.count(ServiceOrder.id)).where(ServiceOrder.created_at >= start, ServiceOrder.created_at < end)).scalar_one()
            if total:
                rows.append((month, total))
        return rows

    

    def count_services_by_month_and_type(
         self,
        year: int,
    ):
        rows = []
        for month in range(1, 13):
            start, end = month_bounds_utc(year, month)
            stmt = (
            select(
                ServiceType.id,
                ServiceType.name,
                func.count(ServiceOrderItem.id),
            )
            .select_from(ServiceOrder)
            .join(
                ServiceOrderItem,
                ServiceOrderItem.service_order_id == ServiceOrder.id,
            )
            .join(
                ServiceType,
                ServiceType.id == ServiceOrderItem.service_type_id,
            )
            .where(
                ServiceOrder.created_at >= start, ServiceOrder.created_at < end
            )
            .group_by(
                ServiceType.id,
                ServiceType.name,
            )
            .order_by(
                ServiceType.id,
            )
        )

            rows.extend((month, *row) for row in self.session.execute(stmt).all())
        return rows


    def get_services_by_employee(self, year: int, month: int):

        stmt = (
            select(
                Employee.id,
                Employee.name,
                ServiceType.id,
                ServiceType.name,
                func.count(ServiceOrderItem.id),
            )
            .select_from(ServiceOrder)
            .join(
                ServiceOrderItem,
                ServiceOrderItem.service_order_id == ServiceOrder.id,
            )
            .join(
                ServiceType,
                ServiceType.id == ServiceOrderItem.service_type_id,
            )
            .join(
                Employee,
                ServiceOrder.employee_id == Employee.id,
            )
            .where(ServiceOrder.created_at >= month_bounds_utc(year, month)[0], ServiceOrder.created_at < month_bounds_utc(year, month)[1])
            .group_by(
                Employee.id,
                Employee.name,
                ServiceType.id,
                ServiceType.name,
            )
            .order_by(
                Employee.name,
                ServiceType.id,
            )
        )

        result = self.session.execute(stmt)

        return result.all()



    def count_service_orders_by_employee(self, year: int, month: int):
        stmt = (
            select(Employee.id, func.count(func.distinct(ServiceOrder.id)))
            .join(Employee, ServiceOrder.employee_id == Employee.id)
            .where(ServiceOrder.created_at >= month_bounds_utc(year, month)[0], ServiceOrder.created_at < month_bounds_utc(year, month)[1])
            .group_by(Employee.id)
        )
        return self.session.execute(stmt).all()
