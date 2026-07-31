import uuid
from sqlalchemy import(
    Column,
    String
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base, TimestampMixin



class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    company_name = Column(String, nullable=False)

    devices = relationship("devices", back_populates="users")
    batteries = relationship("batteries", back_populates="users")
    bookings = relationship("bookings", back_populates="users")