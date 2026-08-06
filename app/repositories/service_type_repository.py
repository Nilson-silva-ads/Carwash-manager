from sqlachemy import select
from sqlalchemy.orm import Session

from app.models.service_type import ServiceType
from app.repositories.base_repository import BaseRepository


class ServiceTypeRepository(BaseRepository[ServiceType]):
    def __init__(self, session: Session):
        super().__init__(session, ServiceType)

    def get_by_name(self, name: str) -> ServiceType | None:
        stmt = select(self.model).where(self.model.name == name)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()