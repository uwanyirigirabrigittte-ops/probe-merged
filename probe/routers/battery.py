import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from probe.schemas.battery import BatteryCreate, BatteryRead, BatteryUpdate


from probe.services.battery import (
   get_battery,
   list_batteries,
   create_battery,
   update_battery,
   delete_battery
)


router = APIRouter(prefix="/batteries", tags=["batteries"])


@router.get("/", response_model=list[BatteryRead])
def route_list_batteries(db: Session = Depends(get_db)):
   return list_batteries(db)


@router.get("/{battery_id}", response_model=BatteryRead)
def route_get_battery(battery_id: uuid.UUID, db: Session = Depends(get_db)):
   db_battery = get_battery(db, battery_id)
   if not db_battery:
       raise HTTPException(status_code=404, detail="Battery record not found")
   return db_battery


@router.post("/", response_model=BatteryRead, status_code=status.HTTP_201_CREATED)
def route_create_battery(data: BatteryCreate, db: Session = Depends(get_db)):
   try:
       return create_battery(db, data)
   except Exception as err:
       raise HTTPException(status_code=400, detail=f"Failed to log battery: {str(err)}")


@router.patch("/{battery_id}", response_model=BatteryRead)
def route_update_battery(battery_id: uuid.UUID, data: BatteryUpdate, db: Session = Depends(get_db)):
   db_battery = update_battery(db, battery_id, data)
   if not db_battery:
       raise HTTPException(status_code=404, detail="Battery record not found")
   return db_battery


@router.delete("/{battery_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_battery(battery_id: uuid.UUID, db: Session = Depends(get_db)):
   success = delete_battery(db, battery_id)
   if not success:
       raise HTTPException(status_code=404, detail="Battery record not found")
