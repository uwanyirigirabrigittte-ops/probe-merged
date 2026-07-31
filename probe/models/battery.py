import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enums import BatteryStatus

from database import Base, TimestampMixin



class Battery(Base, TimestampMixin):
    __tablename__ = "batteries"

    battery_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chemistry = Column(String, nullable=False)
    recycler_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.device_id"), nullable=False)
    status = Column(Enum(BatteryStatus), nullable=False)
    category = Column(String, nullable=False)



    recycler = relationship("users", back_populates="batteries")
    device = relationship("devices", back_populates="batteries")
    sensor_readings = relationship("sensor_readings", back_populates="batteries")
    bookings = relationship("bookings", back_populates="batteries")