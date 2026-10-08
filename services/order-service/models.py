from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base
import enum
from sqlalchemy.orm import relationship

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(Enum(OrderStatus), default= OrderStatus.PENDING, nullable= False)
    total = Column(Integer, nullable= False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable= False)
    updated_at = Column(DateTime, default= datetime.utcnow , onupdate= datetime.utcnow, nullable= False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "orders_items"

    id = Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable= False)
    price = Column(Integer, nullable= False)
    
    order = relationship("Order", back_populates="items")