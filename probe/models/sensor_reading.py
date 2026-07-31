import uuid
from sqlalchemy import (
    Column,
    Float,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



from database import Base, TimestampMixin



class SensorReading(Base, TimestampMixin):
    __tablename__ = "sensor_readings"

    sensor_reading_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.device_id"), nullable=False)
    battery_id = Column(UUID(as_uuid=True), ForeignKey("batteries.battery_id"), nullable=False)
    temp = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    state_of_health = Column(Float, nullable=False)



    device = relationship("devices", back_populates="sensor_readings")
    battery = relationship("batteries", back_populates="sensor_readings")