from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Schema untuk membuat user baru (register)
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["john_doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, examples=["secret123"])
    full_name: Optional[str] = Field(None, max_length=100, examples=["John Doe"])


# Schema untuk response user (tanpa password)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# Schema untuk login
class UserLogin(BaseModel):
    username: str = Field(..., examples=["john_doe"])
    password: str = Field(..., examples=["secret123"])


# Schema token JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
