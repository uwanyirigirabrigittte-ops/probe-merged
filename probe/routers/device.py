import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from probe.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from probe.services.device import (
    get_device,
    get_device_by_serial_number,
    list_devices,
    create_device,
    update_device,
    delete_device
)


router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[DeviceRead])
def route_list_devices(db: Session = Depends(get_db)):
    return list_devices(db)


@router.get("/{device_id}", response_model=DeviceRead)
def route_get_device(device_id: uuid.UUID, db: Session = Depends(get_db)):
    return get_device(db, device_id)


@router.get("/by-serial-number/{serial_number}", response_model=DeviceRead)
def route_get_device_by_serial_number(serial_number: str, db: Session = Depends(get_db)):
    return get_device_by_serial_number(db, serial_number)


@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def route_create_device(data: DeviceCreate, db: Session = Depends(get_db)):
    return create_device(db, data)


@router.patch("/{device_id}", response_model=DeviceRead)
def route_update_device(device_id: uuid.UUID, data: DeviceUpdate, db: Session = Depends(get_db)):
    return update_device(db, device_id, data)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_device(device_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_device(db, device_id)