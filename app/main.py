from fastapi import FastAPI
from app.routes.employee_route import router as employee_route

app = FastAPI( 
    title="CarWash Maanger",
    version="1.0.0",
    description="API para gerenciamento do post de Lavagem"
)

app.include_router(employee_route)

