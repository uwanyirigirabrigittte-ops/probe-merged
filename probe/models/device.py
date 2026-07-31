import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



from database import Base, TimestampMixin



class Device(Base, TimestampMixin):
    __tablename__ = "devices"

    device_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recycler_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    error_code = Column(String, nullable=True)
    channel = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)



    user = relationship("users", back_populates="devices")
    batteries = relationship("batteries", back_populates="devices")
    sensor_readings = relationship("sensor_readings", back_populates="devices")