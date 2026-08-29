from fastapi import APIRouter, Depends

from app.dependencies.employee_dependencies import get_current_admin, get_current_employee
from app.dependencies.service_type_dependencies import get_service_type_service

from app.models.employee import Employee

from app.schemas.service_type_schema import (
    ServiceTypeCreateSchema,
    ServiceTypeResponseSchema,
    ServiceTypeUpdateSchema,
)
from app.services.service_type_service import ServiceTypeService

router = APIRouter(
    prefix="/service-types",
    tags=["Service Types"],
)


@router.post(
    "",
    response_model=ServiceTypeResponseSchema,
)
def create_service_type(
    service_type_data: ServiceTypeCreateSchema,
    current_admin: Employee = Depends(get_current_admin),
    service: ServiceTypeService = Depends(get_service_type_service),
):
    service_type = service.create_service_type(
        name=service_type_data.name,
    )

    return ServiceTypeResponseSchema.model_validate(service_type)


@router.get(
    "",
    response_model=list[ServiceTypeResponseSchema],
)
def get_service_types(
    current_employee: Employee = Depends(get_current_employee),
    service: ServiceTypeService = Depends(get_service_type_service),
):
    service_types = service.get_all_service_types()

    return [
        ServiceTypeResponseSchema.model_validate(service_type)
        for service_type in service_types
    ]


@router.get(
    "/{service_type_id}",
    response_model=ServiceTypeResponseSchema,
)
def get_service_type_by_id(
    service_type_id: int,
    current_admin: Employee = Depends(get_current_admin),
    service: ServiceTypeService = Depends(get_service_type_service),
):
    service_type = service.get_service_type_by_id(service_type_id)

    return ServiceTypeResponseSchema.model_validate(service_type)


@router.put(
    "/{service_type_id}",
    response_model=ServiceTypeResponseSchema,
)
def update_service_type(
    service_type_id: int,
    service_type_data: ServiceTypeUpdateSchema,
    current_admin: Employee = Depends(get_current_admin),
    service: ServiceTypeService = Depends(get_service_type_service),
):
    service_type = service.update_service_type(
        service_type_id=service_type_id,
        name=service_type_data.name,
    )

    return ServiceTypeResponseSchema.model_validate(service_type)


@router.patch(
    "/{service_type_id}/deactivate",
    response_model=ServiceTypeResponseSchema,
)
def deactivate_service_type(
    service_type_id: int,
    current_admin: Employee = Depends(get_current_admin),
    service: ServiceTypeService = Depends(get_service_type_service),
):
    service_type = service.deactivate_service_type(service_type_id)

    return ServiceTypeResponseSchema.model_validate(service_type)


@router.patch(
    "/{service_type_id}/activate",
    response_model=ServiceTypeResponseSchema,
)
def activate_service_type(
    service_type_id: int,
    current_admin: Employee = Depends(get_current_admin),
    service: ServiceTypeService = Depends(get_service_type_service),
):

    service_type = service.activate_service_type(service_type_id)

    return ServiceTypeResponseSchema.model_validate(service_type)