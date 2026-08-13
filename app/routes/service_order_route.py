from fastapi import APIRouter, Depends, status

from app.dependencies.service_order_dependencies import get_service_order_service
from app.dependencies.employee_dependecies import ger_current_employee

from app.models.employee import Employee

from app.schemas.service_order_schema import ServiceOrderCreateSchema, ServiceOrderResponseSchema

from app.services.service_order_service import ServiceOrderService


router = APIRouter(
    prefix="/service-orders", tags=["Service Orders"]
)

@router.post("", response_models=ServiceOrderResponseSchema, status_code=status.HTTP_201_CREATED)

def create_service_order( 
      service_oder_data: ServiceOrderCreateSchema,
      current_employee:Employee = Depends(get_current_employee),
      service: ServiceOrderService = Depends(get_service_order_service) ):

    return service.create_service_order( plate=service_order_data.plate, employee_id=current_employee.id, service_type_ids=service_oder_data.service_type_ids )