from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity : int 
    price: int 

class OrderCreate(BaseModel):
    user_id: UUID
    items: list[OrderItemCreate]

class OrderItemRead(BaseModel):
    id : UUID
    product_id: UUID
    quantity: int
    price: int
    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id:UUID
    user_id: UUID
    status: str
    total: int
    items: list[OrderItemRead]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)