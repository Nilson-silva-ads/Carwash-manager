from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from collections.abc import Generator

from app.database.config import DATABASE_URL


#Cria a concxão com o banco.
engine = create_engine(
    DATABASE_URL,
    echo=True, #faz o SQLAlchemy  mostrar no terminal todo o SQL que ele executa.
)

#Cria uma nova sessão, sempre que precisar conversar com o banco.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal() #cria uma nova sessão.

    try:
        yield db #Entrega essa sessão para a rota, enquanto a rota estiver executando, ela usa essa sessão. Quando a rota terminar continua no finally.
    finally:
        db.close() #A conexão sera fechada, idependentemente de ter dado certo ou errado.