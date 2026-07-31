import enum

class UserType(str,enum.Enum):
    RECYCLER = "RECYCLER"
    UPS_COMPANY = "UPS_COMPANY"

class BatteryStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    PROCESSING = "PROCESSING"

class BookingStatus(str,enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"

class DeviceStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    
