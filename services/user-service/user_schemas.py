from pydantic import BaseModel, ConfigDict, Field, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    name: str  = Field(min_length=1, max_length=100)
    email: EmailStr 
    password : str = Field(min_length=8, max_length=120)

class UserRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str 
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)