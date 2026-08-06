from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from typing import cast

from probe.repositories.device import DeviceRepository
from probe.repositories.user import UserRepository
from probe.models.enums import UserType
from probe.schemas.device import DeviceCreate, DeviceUpdate
from probe.models.user import User


def list_devices(db: Session, current_user: User):
    return DeviceRepository.get_by_recycler_id(db, current_user.user_id)


def get_device(db: Session, device_id: UUID, current_user: User):
    device = DeviceRepository.get_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    if device.recycler_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return device


def create_device(db: Session, data: DeviceCreate, current_user: User):
    if cast(UserType, current_user.user_type) != UserType.RECYCLER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Violation: Only registered recycler entities can manage screening hardware units."
        )

    clean_channel = data.channel.strip()
    clean_status = data.status.value.strip() if hasattr(data.status, 'value') else str(data.status).strip()

    if not clean_channel or not clean_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required hardware configuration values cannot be empty or whitespaces."
        )

    dumped_data = data.model_dump()
    dumped_data["channel"] = clean_channel
    dumped_data["status"] = clean_status
    if data.description:
        dumped_data["description"] = data.description.strip()
    if data.error_code:
        dumped_data["error_code"] = data.error_code.strip()

    dumped_data["recycler_id"] = current_user.user_id

    return DeviceRepository.create(db, dumped_data)


def update_device(db: Session, device_id: UUID, data: DeviceUpdate, current_user: User):
    device = get_device(db, device_id, current_user)
    return DeviceRepository.update(db, device, data.model_dump(exclude_unset=True))


def delete_device(db: Session, device_id: UUID, current_user: User):
    device = get_device(db, device_id, current_user)
    return DeviceRepository.delete(db, device)
