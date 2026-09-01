from pydantic import BaseModel, Field, ConfigDict

class EmployeeCreateSchema(BaseModel):

    name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6)
    is_admin: bool = False

class EmployeeResponseSchema(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    is_admin: bool
    is_active: bool

class EmployeeUpdateSchema(BaseModel):

    name: str | None = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=1, max_length=50)