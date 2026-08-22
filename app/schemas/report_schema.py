from pydantic import BaseModel



class ServiceReportItemSchema(BaseModel):
    service_type_id: int
    name: str
    total: int


class ServiceOrderReportResponseSchema(BaseModel):
    total_service_orders: int
    services: list[ServiceReportItemSchema]