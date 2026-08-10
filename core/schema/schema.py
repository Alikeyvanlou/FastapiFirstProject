from pydantic import BaseModel, Field

class Cast(BaseModel):
    description: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0.1)

class CastCreate(Cast):
    pass

class CastResponse(Cast):
    id: int

class CastUpdate(Cast):
    pass

class CastDeleteResponse(BaseModel):
    message: str
