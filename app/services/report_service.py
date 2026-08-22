from datetime import datetime

from app.repositories.report_repository import ReportRepository


class ReportService:

    def __init__( self, report_repository: ReportRepository ):
        self.report_repository = report_repository


    def get_service_order_report(
        self, 
        start_date: datetime,
        end_date: datetime,
    ): 

        if start_date > end_date:
            raise ValueError( "A data inicial não pode ser maior que data final." )
        
        total_service_orders = self.report_repository.count_service_orders(
            start_date=start_date,
            end_date = end_date,
        )

        services_by_type = self.report_repository.count_services_by_type(
            start_date = start_date,
            end_date = end_date,
        )

        return {
            "total_service_orders": total_service_orders,
            "services": [
                {
                    "service_type_id": service_type_id,
                    "name": name,
                    "total": total,
                }
                for service_type_id, name, total in services_by_type
            ],
        }