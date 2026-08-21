
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class EmployeeServiceOrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class ServiceTypeOrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ServiceOrderCreateSchema(BaseModel):
    plate: str = Field(..., min_length=1, max_length=10)
    service_type_ids: list[int] = Field(..., min_length=1)



class ServiceOrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    service_order_id: int
    service_type_id: int
    service_type: ServiceTypeOrderResponseSchema

class ServiceOrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plate: str
    employee_id: int
    employee: EmployeeServiceOrderSchema
    created_at: datetime
    items: list[ServiceOrderItemResponseSchema]


class ServiceOrderFilterSchema(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    plate: str | None = Field (
        default=None,
        min_length=1,
        max_length=10,
    )
    employee_id: int | None = None
