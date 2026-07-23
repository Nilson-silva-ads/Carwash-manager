from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.employee import Employee
from app.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):

    def __init__(self, session: Session):
        super().__init__(session, Employee)

    
    def get_by_username(self, username: str) -> Employee | None:
        stmt = select(self.model).where(self.model.username == username)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()