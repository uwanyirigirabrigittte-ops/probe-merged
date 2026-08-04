from database import Base, engine
from fastapi import FastAPI
from probe.routers import router


Base.metadata.create_all(bind=engine)
app = FastAPI(title="probe API", version="1.0.0")

app.include_router(router)