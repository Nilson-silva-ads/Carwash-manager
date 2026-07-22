from typing import Generic, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T") #pode receber qualquer tipo modelo.


class BaseRepository(Generic[T]):  #Estamos dizendo que essa classe trabalha com qualquer tipo [T].
    """ Classe base para o acesso ao banco de dados. """

    def __init__(self, session: Session, model: type[T]):  #em model: type[T], significa que o parametro model deve ser uma clase do tipo T.
        self.session = session
        self.model = model

    def create(self, entity: T) -> T:
        self.session.add(entity)  #Coloca o objeto na sessão do SQLAlchemy, ainda não gravou no banco.
        self.session.commit()  #Agora sim o SQLAlchemy envia a operação para o banco de dados.
        self.session.refresh(entity)  #Atualiza o objeto com os dados que o banco gerou automaticamente.
        return entity  #retorna o mesmo objeto atualizado.

    def get_by_id(self, id: int) - T | None:
        stmt = select(self.model).where(self.model.id == id)  #Cria uma consulta e adiciona o filtro.
        result = self.session.execute(stmt)  #executa o banco de dados.
        return result.scalar_one_or_none()  #retorna o objeto encontrado ou None se não existir nunhum registro co aquele ID.

    def get_all(self) -> list(T):
        stmt = select(self.model)
        result = self.session.execute(stmt)
        return result.scalar().all()  #em saclar pegamos apenas o objeto do modelo e usando o all transformamos tudo em uma lista.

    def update(self, entity: T) -> T:
        entity = self.session.merge(entity)  #cria a estancia entity e usa o merge para atualizar.
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, id: int) -> bool:
        entity = self.get_by_id(id)
        
        if entity is None:
            return False

        self.session.delete(entity)
        self.session.commit()

        return True