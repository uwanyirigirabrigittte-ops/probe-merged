from database import Base, engine
from fastapi import FastAPI
import probe.models as models


Base.metadata.create_all(bind=engine)
app = FastAPI(title="probe API", version="1.0.0")

from probe.routers import(
    booking_router
)

app.include_router(booking_router)
