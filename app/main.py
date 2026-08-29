from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.core.exception_handlers import register_exception_handlers
from app.core.routes import employee_router, auth_router, service_order_router, service_type_router, report_router


app = FastAPI( 
    title="CarWash Manager",
    version="1.0.0",
    description="API para gerenciamento do posto de Lavagem"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(employee_router)

app.include_router(auth_router)

app.include_router(service_order_router)

app.include_router(service_type_router)

app.include_router(report_router)