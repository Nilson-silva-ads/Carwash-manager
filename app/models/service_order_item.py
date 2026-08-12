from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base_model import BaseModel

from typing import TYPE_CHECKING

class ServiceOrderItem(BaseModel):
    "Modelo que representa um item de serviço prestado."
    __tablename__ = "service_order_items"

    service_order_id: Mapped[int] = mapped_column(ForeignKey("service_orders.id"), nullable=False) #Define service_order_id como chave estrangeira para a tabela service_orders, sem permitir valores nulos.
    service_type_id: Mapped[int] = mapped_column(ForeignKey("service_types.id"), nullable=False) #Define service_type_id como chave estrangeira para a tabela service_types, sem permitir valores nulos.

    service_order: Mapped["ServiceOrder"] = relationship(back_populates="items") #Define relacionamento com a tabela service_orders, permitindo acesso aos dados do serviço prestado associado a cada item de serviço.
    service_type: Mapped["ServiceType"] = relationship(back_populates="service_order_items") #Define relacionamento com a tabela service_types, permitindo acesso aos dados do tipo de serviço associado a cada item de serviço.

if TYPE_CHECKING: 
    from app.models.service_order import ServiceOrder
    from app.models.service_type import ServiceType