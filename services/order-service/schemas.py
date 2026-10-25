from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity : int = Field(gt= 0) # строго больше нуля
    price: int = Field(ge = 0) # больше или равно нулю

class OrderCreate(BaseModel):
    user_id: UUID
    items: list[OrderItemCreate] = Field(min_length=1)

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