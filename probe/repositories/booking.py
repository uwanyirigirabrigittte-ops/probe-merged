import uuid


from sqlalchemy.orm import Session


from probe.models.booking import Booking




class BookingRepository:
   def __init__(self):
       self.model = Booking


   def get_by_id(self, db: Session, id: uuid.UUID):
       return db.get(self.model, id)


   def get_all(self, db: Session):
       return db.query(self.model).all()


   def create(self, db: Session, data: dict):
       booking = self.model(**data)
       db.add(booking)
       db.commit()
       db.refresh(booking)
       return booking


   def update(self, db: Session, db_obj: Booking, data: dict):
       for field, value in data.items():
           setattr(db_obj, field, value)
       db.commit()
       db.refresh(db_obj)
       return db_obj


   def delete(self, db: Session, db_obj: Booking):
       db.delete(db_obj)
       db.commit()
       return True


booking_repository = BookingRepository()
