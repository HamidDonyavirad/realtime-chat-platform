from pydantic import BaseModel, EmailStr,Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8,max_length=72)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_verified: bool

