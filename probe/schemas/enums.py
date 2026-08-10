import enum

class UserType(str,enum.Enum):
   RECYCLER = "RECYCLER"
   UPS_COMPANY = "UPS_COMPANY"

class DeviceStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


