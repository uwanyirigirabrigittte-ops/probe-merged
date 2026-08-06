import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from probe.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from probe.services.device import (
    get_device,
    list_devices,
    create_device,
    update_device,
    delete_device
)
from probe.dependencies import get_current_user
from probe.models.user import User


router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[DeviceRead])
def route_list_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_devices(db, current_user)


@router.get("/{device_id}", response_model=DeviceRead)
def route_get_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_device(db, device_id, current_user)


@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def route_create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_device(db, data, current_user)


@router.patch("/{device_id}", response_model=DeviceRead)
def route_update_device(
    device_id: uuid.UUID,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_device(db, device_id, data, current_user)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_device(db, device_id, current_user)
