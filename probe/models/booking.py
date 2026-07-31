import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



from database import Base, TimestampMixin



class Booking(Base, TimestampMixin):
    __tablename__ = "bookings"

    booking_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    battery_id = Column(UUID(as_uuid=True), ForeignKey("batteries.battery_id"), nullable=False)
    status = Column(String, nullable=False)

    buyer = relationship("users", back_populates="bookings")
    battery = relationship("batteries", back_populates="bookings")