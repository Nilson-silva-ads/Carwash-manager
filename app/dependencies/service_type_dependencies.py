from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.repositories.service_type_repository import ServiceTypeRepository
from app.services.service_type_service import ServiceTypeService



def get_service_type_service( session: Session = Depends(get_db)) -> ServiceTypeService:

    repository = ServiceTypeRepository(session)
    service = ServiceTypeService(repository)

    return service