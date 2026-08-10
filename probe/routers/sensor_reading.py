from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from probe.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse, SensorReadingUpdate
from probe.services.sensor_reading import SensorReadingService


router = APIRouter(prefix="/v1/sensor-readings", tags=["Sensor Readings"])


@router.post("/", response_model=SensorReadingResponse, status_code=status.HTTP_201_CREATED)
def record_hardware_telemetry(
   payload: SensorReadingCreate,
   db: Session = Depends(get_db)
):
   return SensorReadingService.create_sensor_reading(db=db, data=payload)


@router.get("/{sensor_reading_id}", response_model=SensorReadingResponse)
def get_sensor_reading(sensor_reading_id: UUID, db: Session = Depends(get_db)):
   return SensorReadingService.get_sensor_reading(db, sensor_reading_id)
@router.patch("/{sensor_reading_id}", response_model=SensorReadingResponse)
def update_sensor_reading(sensor_reading_id: UUID, payload: SensorReadingUpdate, db: Session = Depends(get_db)):
   return SensorReadingService.update_sensor_reading(db, sensor_reading_id, payload)






@router.delete("/{sensor_reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_reading(sensor_reading_id: UUID, db: Session = Depends(get_db)):
   SensorReadingService.delete_sensor_reading(db, sensor_reading_id)
   return None
