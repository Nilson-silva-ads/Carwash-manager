from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.report_repository import ReportRepository
from app.services.report_service import ReportService


def get_report_service(
    session: Session = Depends(get_db),
) -> ReportService:

    repository = ReportRepository(session)
    service = ReportService(repository)

    return service