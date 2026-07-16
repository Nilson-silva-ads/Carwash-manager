from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


from typing import TYPE_CHECKING


class Service(BaseModel):
    """Modelo que representa um serviço prestado."""
    __tablename__ = "services"

    plate: Mapped[str] = mapped_column(String(10), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    service_type_id: Mapped[int] = mapped_column(ForeignKey("service_types.id"), nullable=False)

    employee: Mapped[Employee] = relationship(back_populates="services")
    service_type: Mapped[ServiceType] = relationship(back_populates="services")


if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.service_type import ServiceType