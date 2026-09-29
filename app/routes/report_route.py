from datetime import datetime

from fastapi import APIRouter, Depends

from app.dependencies.employee_dependencies import get_current_admin
from app.dependencies.report_dependencies import get_report_service

from app.models.employee import Employee

from app.schemas.report_schema import ServiceOrderReportResponseSchema, MonthlyServiceOrderReportSchema, EmployeeMonthlyReportResponseSchema, DashboardReportResponseSchema

from app.services.report_service import ReportService



router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

@router.get(
    "/service-orders",
    response_model=ServiceOrderReportResponseSchema,
)
def get_service_order_report(
    start_date: datetime,
    end_date: datetime,
    employee_id: int | None = None,
    service_type_id: int | None = None,
    current_admin: Employee = Depends(get_current_admin),
    service: ReportService = Depends(get_report_service),
):
    return service.get_service_order_report(
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id,
        service_type_id=service_type_id,
    )


@router.get(
    "/monthly",
    response_model=list[MonthlyServiceOrderReportSchema],
)
def get_monthly_service_order_report(
    year: int,
    current_admin: Employee = Depends(get_current_admin),
    service: ReportService = Depends(get_report_service),
):

    return service.get_monthly_service_order_report(year=year)

@router.get("/monthly/employee", response_model=EmployeeMonthlyReportResponseSchema)
def get_employee_monthly_report(
    year: int,
    month: int,
    current_admin: Employee = Depends(get_current_admin),
    service: ReportService = Depends(get_report_service),
):
    return service.get_employee_monthly_report(year=year, month=month)

@router.get(
    "/dashboard",
    response_model=DashboardReportResponseSchema,
)
def get_dashboard_report(
    current_admin: Employee = Depends(get_current_admin),
    service: ReportService = Depends(get_report_service),
):
    return service.get_dashboard_report()
