from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
import math


from ..repositories import SensorReadingRepository, BatteryRepository, DeviceRepository
from ..schemas.sensor_reading import SensorReadingCreate, SensorReadingUpdate


R_NEW = 0.020  
R_DEAD = 0.120 


class SensorReadingService:


   @staticmethod
   def get_sensor_reading(db: Session, sensor_reading_id: UUID):
       reading = SensorReadingRepository.get_by_id(db, sensor_reading_id)
       if not reading:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Telemetry entry not found"
           )
       return reading


   @staticmethod
   def list_sensor_readings(db: Session):
       return SensorReadingRepository.get_all(db)


   @staticmethod
   def create_sensor_reading(db: Session, data: SensorReadingCreate):
       device = DeviceRepository.get_by_id(db, data.device_id)
       battery = BatteryRepository.get_by_id(db, data.battery_id)
       if not device or not battery:
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Hardware Authentication Failure: Unmapped device or battery parameters."
           )


       if data.temp > 55.0:
           BatteryRepository.update(db, battery, {"status": "INACTIVE"})
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Emergency Cutoff: High-temperature hazard detected. Slot offline and asset quarantined."
           )




       if data.current <= 0 or data.v_rest < data.v_load:
           soh_percentage = 0.0
       else:
           try:
  
               r_i = (data.v_rest - data.v_load) / data.current
               soh_fraction = (R_DEAD - r_i) / (R_DEAD - R_NEW)
               soh_percentage = max(0.0, min(100.0, soh_fraction * 100.0))
              
               if math.isnan(soh_percentage):
                   soh_percentage = 0.0
           except ZeroDivisionError:
               soh_percentage = 0.0


       if soh_percentage > 65.0:
           battery_updates = {"category": "A", "status": "AVAILABLE"}
       elif 50.0 <= soh_percentage <= 65.0:
           battery_updates = {"category": "B", "status": "AVAILABLE"}
       else:
           battery_updates = {"category": "C", "status": "PROCESSING"}


       BatteryRepository.update(db, battery, battery_updates)
       dumped_data = data.model_dump()
       dumped_data["state_of_health"] = soh_percentage
       dumped_data["voltage"] = dumped_data.pop("v_load")
       del dumped_data["v_rest"]


       return SensorReadingRepository.create(db, dumped_data)


   @staticmethod
   def update_sensor_reading(db: Session, sensor_reading_id: UUID, data: SensorReadingUpdate):
       reading = SensorReadingService.get_sensor_reading(db, sensor_reading_id)
       update_data = data.model_dump(exclude_unset=True)


       v_rest = data.v_rest
       v_load = data.v_load
       current = data.current if data.current is not None else reading.current


       if v_rest is not None and v_load is not None:
           if current <= 0 or v_rest < v_load:
               soh_percentage = 0.0
           else:
               try:
                   r_i = (v_rest - v_load) / current
                   soh_fraction = (R_DEAD - r_i) / (R_DEAD - R_NEW)
                   soh_percentage = max(0.0, min(100.0, soh_fraction * 100.0))
                   if math.isnan(soh_percentage):
                       soh_percentage = 0.0
               except ZeroDivisionError:
                   soh_percentage = 0.0


           update_data["state_of_health"] = soh_percentage
           update_data["voltage"] = v_load
           del update_data["v_rest"]
           del update_data["v_load"]


           if soh_percentage > 65.0:
               battery_updates = {"category": "A", "status": "AVAILABLE", "price": 6000.0}
           elif 50.0 <= soh_percentage <= 65.0:
               battery_updates = {"category": "B", "status": "AVAILABLE", "price": 3440.0}
           else:
               battery_updates = {"category": "C", "status": "PROCESSING", "price": 1760.0}


           battery = BatteryRepository.get_by_id(db, reading.battery_id)
           if battery:
               BatteryRepository.update(db, battery, battery_updates)


       if data.temp is not None and data.temp > 55.0:
           battery = BatteryRepository.get_by_id(db, reading.battery_id)
           if battery:
               BatteryRepository.update(db, battery, {"status": "INACTIVE"})
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Emergency Cutoff: High-temperature hazard detected. Slot offline and asset quarantined."
           )


       return SensorReadingRepository.update(db, reading, update_data)


   @staticmethod
   def delete_sensor_reading(db: Session, sensor_reading_id: UUID):
       reading = SensorReadingService.get_sensor_reading(db, sensor_reading_id)
       SensorReadingRepository.delete(db, reading)
       return None



