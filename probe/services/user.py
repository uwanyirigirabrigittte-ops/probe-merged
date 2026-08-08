from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from probe.repositories.user import user_repository
from probe.schemas.user import UserCreate
from probe.services.auth import hash_password, verify_password, create_access_token


def authenticate_user(db: Session, email: str, password: str):
    clean_email = email.strip().lower()
    user = user_repository.get_by_email(db, clean_email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    token = create_access_token(user.user_id, user.user_type)
    return {"access_token": token, "token_type": "bearer"}


def get_user(db: Session, user_id: UUID, current_user):
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="You can only view your own account")
    db_user = user_repository.get_by_id(db, str(user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail="User record not found")
    return db_user


def create_user(db: Session, data: UserCreate):
    clean_email = data.email.strip().lower()

    if not clean_email or not data.password_hash.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required authentication credentials cannot be empty."
        )

    if len(data.password_hash) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Security policy violation: Password must be at least 8 characters long."
        )

    clean_user_type = data.user_type.value.strip() if hasattr(data.user_type, 'value') else str(data.user_type).strip()
    if clean_user_type not in ["RECYCLER", "UPS_COMPANY"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid system operational role requested."
        )

    existing_user = user_repository.get_by_email(db, clean_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user profile with this email address is already registered."
        )

    user_dict = data.model_dump()
    user_dict["email"] = clean_email
    user_dict["user_type"] = clean_user_type
    user_dict["password_hash"] = hash_password(user_dict["password_hash"])

    return user_repository.create(db, user_dict)

def delete_user(db: Session, user_id: UUID, current_user):
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="You can only delete your own account")

    db_user = user_repository.get_by_id(db, str(user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail="User record not found")

    user_repository.delete(db, db_user)