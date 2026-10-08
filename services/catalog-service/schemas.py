from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: int
    stock: int = 0
    category: str | None = None

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock: int | None = None
    category: str | None = None

class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True) # нужно когда ответ от сервара

    id: UUID
    name: str
    description: str | None
    price: int
    stock: int
    category: str | None
    created_at: datetime
    updated_at: datetime