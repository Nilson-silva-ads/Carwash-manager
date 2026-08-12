
from fastapi import Depends
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.dependencies.employee_dependencies import get_current_employee
from app.models.base_model import BaseModel
from app.models.employee import Employee


class ServiceOrderCreateSchema(BaseModel):
    plate: str = Field(..., length=1, max_length=10)
    service_type_ids: list[int] = Field(..., min_length=1)


class ServiceTypeOrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class ServiceOrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    service_order_id: int
    service_type_id: int

class ServiceOrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plate: str
    employee_id: int
    created_at: datetime
    items: list[ServiceOrderItemResponseSchema]
    created_at: datetime = Field(default_factory=datetime.utcnow)                                                          