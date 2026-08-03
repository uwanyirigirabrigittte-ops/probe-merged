import uuid


from sqlalchemy.orm import Session


from probe.models.battery import Battery




class BatteryRepository:
   def __init__(self):
       self.model = Battery


   def get_by_id(self, db: Session, id: uuid.UUID):
       return db.get(self.model, id)


   def get_all(self, db: Session):
       return db.query(self.model).all()


   def create(self, db: Session, data: dict):
       battery = self.model(**data)
       db.add(battery)
       db.commit()
       db.refresh(battery)
       return battery


   def update(self, db: Session, db_obj: Battery, data: dict):
       for field, value in data.items():
           setattr(db_obj, field, value)
       db.commit()
       db.refresh(db_obj)
       return db_obj


   def delete(self, db: Session, db_obj: Battery):
       db.delete(db_obj)
       db.commit()


battery_repository = BatteryRepository()
