from datetime import datetime

from fastapi import APIRouter, Depends

from app.dependencies.employee_dependencies import get_current_employee
from app.dependencies.report_dependencies import get_report_service

from app.models.employee import Employee

from app.schemas.report_schema import ServiceOrderReportResponseSchema, MonthlyServiceOrderReportSchema

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
    current_employee: Employee = Depends(get_current_employee),
    service: ReportService = Depends(get_report_service),
):
    return service.get_service_order_report(
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/monthly",
    response_model=list[MonthlyServiceOrderReportSchema],
)
def get_monthly_service_order_report(
    year: int,
    current_employee: Employee = Depends(get_current_employee),
    service: ReportService = Depends(get_report_service),
):

    return service.get_monthly_service_order_report( year=year) 