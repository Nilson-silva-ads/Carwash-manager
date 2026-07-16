from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.service import Service

class Employee(BaseModel):
    """ Classe que representa um funcionario """
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        )
    
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        )

    services: Mapped[list["Service"]] = relationship(back_populates="employee")

