import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from probe.schemas.user import UserCreate, UserRead, UserUpdate

from probe.services.user import (
    get_user,
    create_user,
    delete_user,
    authenticate_user
)
from probe.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def route_create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, data)
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(err)}")


@router.post("/login")
def route_login(email: str, password: str, db: Session = Depends(get_db)):
    return authenticate_user(db, email, password)


@router.get("/{user_id}", response_model=UserRead)
def route_get_user(user_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="You can only view your own account")
    db_user = get_user(db, str(user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail="User record not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_user(user_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="You can only delete your own account")
    success = delete_user(db, str(user_id))
    if not success:
        raise HTTPException(status_code=404, detail="User record not found")