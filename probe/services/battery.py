from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from probe.repositories.battery import battery_repository
from probe.repositories.user import user_repository
from probe.schemas.battery import BatteryCreate, BatteryUpdate
from probe.services.battery_utils import get_pybamm_parameters, verify_label_plausibility
from probe.models.enums import BatteryStatus


def evaluate_and_grade_battery(db: Session, battery_id:UUID, claimed_capacity_mah: float):
    db_battery = battery_repository.get_by_id(db, battery_id)
    if not db_battery:
        return None

    is_legit = verify_label_plausibility(db_battery.category, claimed_capacity_mah)
    if not is_legit:
        return battery_repository.update(db, db_battery, {"status": BatteryStatus.PROCESSING})

    pybamm_params = get_pybamm_parameters(db_battery.chemistry)
    if pybamm_params and claimed_capacity_mah <= 3500:
        calculated_status = BatteryStatus.AVAILABLE
    else:
        calculated_status = BatteryStatus.PROCESSING

    return battery_repository.update(db, db_battery, {"status": calculated_status})


def get_battery(db: Session, battery_id: UUID):

   battery = battery_repository.get_by_id(db, battery_id)
   if not battery:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Battery asset target not found")
   return battery



def list_batteries(db: Session, search: str = ""):
    all_batteries = battery_repository.get_all(db)
    allowed_variants = ["Lithium-ion", "NMC", "LFP"]
    lithium_only = [b for b in all_batteries if b.chemistry in allowed_variants]
    return lithium_only




def create_battery(db: Session, data: BatteryCreate):
   clean_chemistry = data.chemistry.strip()
   clean_status = data.status.value.strip() if hasattr(data.status, 'value') else str(data.status).strip()
   clean_category = data.category.strip()

   if not clean_chemistry or not clean_status or not clean_category:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Battery profile fields cannot consist of empty parameters."
       )



   recycler = user_repository.get_by_id(db, data.recycler_id)
   if not recycler or recycler.user_type != "RECYCLER":
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Invalid asset assignment: Target recycler profile must exist and hold proper credentials."
       )

   dumped_data = data.model_dump()
   dumped_data["chemistry"] = clean_chemistry
   dumped_data["status"] = clean_status
   dumped_data["category"] = clean_category

   return battery_repository.create(db, dumped_data)



def update_battery(db: Session, battery_id: UUID, data: BatteryUpdate):
   battery = get_battery(db, battery_id)
   return battery_repository.update(db, battery, data.model_dump(exclude_unset=True))



def delete_battery(db: Session, battery_id: UUID):
   battery = get_battery(db, battery_id)
   return battery_repository.delete(db, battery)
