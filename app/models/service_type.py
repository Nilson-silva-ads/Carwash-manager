from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.service import Service

class ServiceType(BaseModel):
    """ Modelo que representa um tipo de serviço. """
    __tablename__ = "service_types"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        )

    services: Mapped[list["Service"]] = relationship(back_populates="service_type")