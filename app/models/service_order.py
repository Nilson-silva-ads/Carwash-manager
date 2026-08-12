from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


from typing import TYPE_CHECKING


class ServiceOrder(BaseModel):
    """Modelo que representa um serviço prestado."""
    __tablename__ = "service_orders"

    plate: Mapped[str] = mapped_column(String(10), nullable=False) #Defice placa de veiculo como string de ate 10 caracteres, sem permitir valores nulos.
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False) #Define employee_id como chave estrangeira para a tabela employees, sem permitir valores nulos.

    employee: Mapped["Employee"] = relationship(back_populates="service_orders") #Define relacionamento com a tabela employees, permitindo acesso aos dados do funcionário associado a cada serviço prestado.

    items: Mapped[list["ServiceOrderItem"]] = relationship(back_populates="service_order") #Define relacionamento com a tabela service_order_items, permitindo acesso aos itens de serviço associados a cada serviço prestado.


if TYPE_CHECKING: #
    from app.models.employee import Employee 
    from app.models.service_order_item import ServiceOrderItem