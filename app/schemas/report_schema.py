from pydantic import BaseModel, Field



class ServiceReportItemSchema(BaseModel):
    service_type_id: int
    name: str
    total: int = Field(..., ge=0)


class ServiceOrderReportResponseSchema(BaseModel):
    total_service_orders: int = Field(..., ge=0)
    services: list[ServiceReportItemSchema]


class MonthlyServiceOrderReportSchema(BaseModel):
    month: int = Field(..., ge=1, le=12)
    total_service_orders: int = Field(..., ge=0)
    services: list[ServiceReportItemSchema]