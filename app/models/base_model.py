from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class BaseModel(Base):
    """ Classe base para todos os modelos de aplicação. """
    __abstract__=True #Diz ao sqlalchemy para não criar uma tabela chamada base_model.

    id: Mapped[int] = mapped_column(primary_key=True) #noda modelagem para melhorar a tipagem, criando o id.

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), #defalut: sempre que um novo registro for criado o SQLAlchemy, preenceherar automaticamente a data e hora atuais.
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc), #onupdate: sempre que um registro for alterado, o campo update_at sera atualizado automaticamente.
    )