from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict
from schemas.cost import CostResponseSchema

class UserBaseSchema(BaseModel):
    id: int
    username: str = Field(..., min_length = 3)
    email: EmailStr
    password: str = Field(..., min_length = 6)

class RegisterUserSchema(BaseModel):

    username: str = Field(..., min_length = 3)
    email: EmailStr
    password: str = Field(..., min_length = 6)
    password_repeat: str = Field(..., min_length = 6)

    @model_validator(mode="after")
    def password_confirm(self):
        if self.password != self.password_repeat :
            raise ValueError("password not match!")
        return self

class EditUserSchema(BaseModel):
    username: str = Field(..., min_length = 3)
    email: EmailStr
    password: str = Field(..., min_length = 6)

class RemoveUserSchema(BaseModel):
    
    message: str

class UserResponseSchema(BaseModel):

    id: int
    username: str
    email: EmailStr
    costs: list[CostResponseSchema]
    model_config = ConfigDict(from_attributes=True)