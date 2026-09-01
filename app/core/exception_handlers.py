from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from app.core.exceptions import EmployeeNotFoundError, EmployeeInactiveError, InvalidCredentialsError, InvalidServiceCombinationError, ServiceTypeInactiveError, ServiceTypeNotFoundError, ServiceOrderWithoutServicesError, UsernameAlreadyExistsError, ServiceTypeAlreadyExistsError, ServiceOrderNotFoundError, AdminRequiredError

def create_error_response( status_code: int, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
    )

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(EmployeeNotFoundError)
    async def employee_not_found_exception_handler(request: Request, exc: EmployeeNotFoundError):
        return create_error_response(status.HTTP_404_NOT_FOUND, exc)


    @app.exception_handler(EmployeeInactiveError)
    async def employee_inactive_exception_handler(request: Request, exc: EmployeeInactiveError):
        return create_error_response(status.HTTP_403_FORBIDDEN, exc)

    
    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsError):
        return create_error_response(status.HTTP_401_UNAUTHORIZED, exc)

    @app.exception_handler(ServiceTypeNotFoundError)
    async def service_type_not_found_exception_handler(request: Request, exc: ServiceTypeNotFoundError):
        return create_error_response(status.HTTP_404_NOT_FOUND, exc)

    @app.exception_handler(ServiceTypeInactiveError)
    async def service_type_inactive_exception_handler(request: Request, exc: ServiceTypeInactiveError):
        return create_error_response(status.HTTP_403_FORBIDDEN, exc)

    @app.exception_handler(ServiceOrderWithoutServicesError)
    async def service_order_without_service_handler(request: Request, exc: ServiceOrderWithoutServicesError):
        return create_error_response(status.HTTP_400_BAD_REQUEST, exc)

    @app.exception_handler(InvalidServiceCombinationError)
    async def invalid_service_combination_handler(request: Request, exc: InvalidServiceCombinationError):
        return create_error_response(status.HTTP_400_BAD_REQUEST, exc)

    @app.exception_handler(UsernameAlreadyExistsError)
    async def username_already_exists_exception_handler(request: Request, exc: UsernameAlreadyExistsError):
        return create_error_response(status.HTTP_409_CONFLICT, exc)

    @app.exception_handler(ServiceTypeAlreadyExistsError)
    async def service_type_already_exists_exception_handler(request: Request, exc: ServiceTypeAlreadyExistsError):
        return create_error_response(status.HTTP_409_CONFLICT, exc)

    @app.exception_handler(ServiceOrderNotFoundError)
    async def service_order_not_found_exception_handler(request: Request, exc: ServiceOrderNotFoundError):
        return create_error_response(status.HTTP_404_NOT_FOUND, exc)


    @app.exception_handler(AdminRequiredError)
    async def admin_required_exception_handler(
        request: Request,
        exc: AdminRequiredError,
    ):
        return create_error_response(status.HTTP_403_FORBIDDEN, exc)
