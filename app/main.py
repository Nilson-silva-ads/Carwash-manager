from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.exception_handlers import register_exception_handlers
from app.core.routes import employee_router, auth_router, service_order_router, service_type_router, report_router


app = FastAPI( 
    title="CarWash Manager",
    version="1.0.0",
    description="API para gerenciamento do posto de Lavagem"
)

configured_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,https://carwash-manager-ttwd-two.vercel.app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in configured_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

register_exception_handlers(app)

app.include_router(employee_router)

app.include_router(auth_router)

app.include_router(service_order_router)

app.include_router(service_type_router)

app.include_router(report_router)
