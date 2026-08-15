import probe.models as models
from database import Base, engine
from fastapi import FastAPI
from probe.routers import user_router
from probe.routers import device_router
from probe.routers import battery_router
from probe.routers import booking_router
from probe.routers import sensor_reading_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="probe API", version="1.0.0")

app.include_router(user_router)
app.include_router(booking_router)
app.include_router(battery_router)
app.include_router(device_router)
app.include_router(sensor_reading_router)
