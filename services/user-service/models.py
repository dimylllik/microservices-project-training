import enum
import uuid

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    role = Column(Enum(UserRole), default = UserRole.USER, nullable = False)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique= True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    password_hash = Column(String(255), nullable=False)