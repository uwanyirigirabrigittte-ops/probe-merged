import enum


class BookingStatus(str,enum.Enum):
   PENDING = "PENDING"
   CONFIRMED = "CONFIRMED"
   CANCELED = "CANCELED"
   COMPLETED = "COMPLETED"
