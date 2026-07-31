from datetime import datetime,timezone
from sqlalchemy import create_engine,Column, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("database_url")
if not database_url:
   raise ValueError("CRITICAL CONFIG ERROR: database_url is missing from the env")

engine = create_engine(database_url, echo=False, future=True)

session = sessionmaker(bind= engine, autocommit = False, autoflush=False)

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)



def get_db():
    db = session()
    try:
      yield db
    finally:
      db.close()