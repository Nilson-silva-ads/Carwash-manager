from fastapi import APIRouter, Depends, status

from app.dependencies.service_order_dependencies import get_service_order_service
from app.dependencies.employee_dependencies import get_current_employee

from app.models.employee import Employee

from app.schemas.service_order_schema import ServiceOrderCreateSchema, ServiceOrderResponseSchema

from app.services.service_order_service import ServiceOrderService


router = APIRouter(
    prefix="/service-orders", tags=["Service Orders"]
)

@router.post("", response_model=ServiceOrderResponseSchema, status_code=status.HTTP_201_CREATED)

def create_service_order( 
      service_order_data: ServiceOrderCreateSchema,
      current_employee:Employee = Depends(get_current_employee),
      service: ServiceOrderService = Depends(get_service_order_service) ):

    return service.create_service_order( plate=service_order_data.plate, employee_id=current_employee.id, service_type_ids=service_order_data.service_type_ids )


@router.get("", response_model=list[ServiceOrderResponseSchema])

def get_service_orders(
    current_employee: Employee = Depends(get_current_employee),
    service: ServiceOrderService = Depends(get_service_order_service),
):
    return service.get_all_service_orders()


@router.get("/plate/{plate}", response_model=list[ServiceOrderResponseSchema] )

def get_service_orders_by_plate( 
    plate: str,
    current_employee: Employee = Depends(get_current_employee),
    service: ServiceOrderService = Depends(get_service_order_service)
):

    return service.get_service_orders_by_plate(plate)



@router.get("/employee/{employee_id}", response_model=list[ServiceOrderResponseSchema] )

def get_service_orders_by_employee(
    employee_id: int,
    current_employee: Employee = Depends(get_current_employee),
    service: ServiceOrderService = Depends(get_service_order_service),
    ):

    return service.get_service_orders_by_employee(employee_id)



@router.get("/{service_order_id}", response_model=ServiceOrderResponseSchema)

def get_service_order_by_id( 
    service_order_id: int,
    current_employee: Employee = Depends(get_current_employee),
    service: ServiceOrderService = Depends(get_service_order_service),
):
        return service.get_service_order_by_id(service_order_id)


