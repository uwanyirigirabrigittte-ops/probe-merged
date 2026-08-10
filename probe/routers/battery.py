import uuid
from fastapi import APIRouter, Depends, status, HTTPException, Query
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
def route_list_batteries(search: str = Query(default=""), db: Session = Depends(get_db)):
   return list_batteries(db, search)


@router.get("/{battery_id}", response_model=BatteryRead)
def route_get_battery(battery_id: uuid.UUID, db: Session = Depends(get_db)):
    return get_battery(db, battery_id)
    


@router.post("/", response_model=BatteryRead, status_code=status.HTTP_201_CREATED)
def route_create_battery(data: BatteryCreate, db: Session = Depends(get_db)):
        return create_battery(db, data)



@router.patch("/{battery_id}", response_model=BatteryRead)
def route_update_battery(battery_id: uuid.UUID, data: BatteryUpdate, db: Session = Depends(get_db)):
    return update_battery(db, battery_id, data)
  


@router.delete("/{battery_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_battery(battery_id: uuid.UUID, db: Session = Depends(get_db)):
     delete_battery(db, battery_id)
 