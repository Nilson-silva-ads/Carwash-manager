from datetime import datetime

from app.repositories.report_repository import ReportRepository
from app.core.timezone import to_utc


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
        
        start_date = to_utc(start_date)
        end_date = to_utc(end_date)
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


    

    def get_monthly_service_order_report(
        self,
        year: int,
    ):

        monthly_data = self.report_repository.count_service_orders_by_month(
            year=year
        )

        services_data = self.report_repository.count_services_by_month_and_type(
            year=year
        )

        report = {
            month: {
                "month": month,
                "total_service_orders": 0,
                "services": [],
            }

            for month in range(1, 13)

        }

        for month, total in monthly_data:
           month = int(month)

           report[month]["total_service_orders"] = total

        
        for month, service_type_id, name, total in services_data:
            month = int(month)
       
            report[month]["services"].append(
                {
                    "service_type_id": service_type_id,
                    "name": name,
                    "total": total,
                }
            )

        return list(report.values())



    def get_employee_monthly_report(
        self,
        year: int,
        month: int,
    ): 
        if month < 1 or month > 12:
            raise ValueError(" O mês deve estar entre 1 e 12.")

        services_data = self.report_repository.get_services_by_employee(
            year=year,
            month=month,
        )
        order_totals = dict(self.report_repository.count_service_orders_by_employee(year, month))

        employees = {}
        total_service_orders = sum(order_totals.values())

        for (
            employee_id,
            employee_name,
            service_type_id,
            service_type_name,
            total,
        ) in services_data:

            if employee_id not in employees:
                employees[employee_id] = {
                    "employee_id": employee_id,
                    "employee_name": employee_name,
                    "total": order_totals.get(employee_id, 0),
                    "services": [],
                }

            employees[employee_id]["services"].append(
                {
                    "service_type_id": service_type_id,
                    "name": service_type_name,
                    "total": total,
                }
            )

        return {
            "year": year,
            "month": month,
            "total_service_orders": total_service_orders,
            "employees": list(employees.values()),
        }
