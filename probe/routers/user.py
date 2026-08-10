from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from probe.schemas.user import UserCreate, UserRead

from probe.services.user import (
    get_user,
    create_user,
    delete_user,
    authenticate_user,
)

from probe.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def route_create_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data)


@router.post("/login")
def route_login(email: str, password: str, db: Session = Depends(get_db)):
    return authenticate_user(db, email, password)


@router.get("/{user_id}", response_model=UserRead)
def route_get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user(db, user_id, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    delete_user(db, user_id, current_user)