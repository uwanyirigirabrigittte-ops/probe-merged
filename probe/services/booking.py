from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID


from probe.repositories.booking import booking_repository
from probe.repositories.user import user_repository
from probe.repositories.battery import battery_repository
from probe.schemas.booking import BookingCreate, BookingUpdate,BookingRead


def get_booking(db: Session, booking_id: UUID):
    booking = booking_repository.get_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking record not found")
    return booking

def list_bookings(db: Session):
   return booking_repository.get_all(db)

def create_booking(db: Session, data: BookingCreate):
   clean_status = data.status.value.strip() if hasattr(data.status, 'value') else str(data.status).strip()
   if not clean_status:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Initial workflow tracking state cannot be empty."
       )


   buyer = user_repository.get_by_id(db, data.user_id)
   if not buyer or buyer.user_type != "UPS_COMPANY": 
       raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Access Denied: Account role unauthorized to initialize purchasing transactions."
       )


   battery = battery_repository.get_by_id(db, data.battery_id)
   if not battery:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="Target hardware entity profile not found."
       )
      
   if battery.status != "AVAILABLE": 
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Transaction Conflict: Asset locked by another operational session."
       )


   battery_repository.update(db, battery, {"status": "PROCESSING"})


   dumped_data = data.model_dump()
   dumped_data["status"] = clean_status
   return booking_repository.create(db, dumped_data)
def update_booking(db: Session, booking_id: UUID, data: BookingUpdate):
   booking = get_booking(db, booking_id)
   return booking_repository.update(db, booking, data.model_dump(exclude_unset=True))


def delete_booking(db: Session, booking_id: UUID):
   booking = get_booking(db, booking_id)
   booking_repository.delete(db, booking)
