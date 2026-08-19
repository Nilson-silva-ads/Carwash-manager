from pydantic import ConfigDict, Field, BaseModel


class ServiceTypeCreateSchema(BaseModel):

    name: str = Field(..., min_length=1, max_length=100)

class ServiceTypeSchema(BaseModel):

    name: str = Field(..., min_length=1, max_length=100)
    

class ServiceTypeResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    is_active: bool

class ServiceTypeUpdateSchema(BaseModel):

    name: str | None = Field(..., min_length=1, max_length=100)
    is_active: bool | None = Field(None)