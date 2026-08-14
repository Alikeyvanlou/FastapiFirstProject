from pydantic import BaseModel, Field

class Cost(BaseModel):
    description: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0.1)

class CostCreateSchema(Cost):
    pass

class CostResponseSchema(Cost):
    id: int

class CostUpdateSchema(Cost):
    pass

class CostDeleteResponseSchema(BaseModel):
    message: str
