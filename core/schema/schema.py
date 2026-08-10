from pydantic import BaseModel, Field

class Cost(BaseModel):
    description: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0.1)

class CostCreate(Cost):
    pass

class CostResponse(Cost):
    id: int

class CostUpdate(Cost):
    pass

class CostDeleteResponse(BaseModel):
    message: str
