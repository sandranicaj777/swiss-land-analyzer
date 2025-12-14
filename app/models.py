from pydantic import BaseModel
from sqlalchemy import Column, String, Float, Boolean, JSON
from sqlalchemy.orm import Mapped
from typing import Optional, Dict, Any
from app.database import Base

class ParcelORM(Base):
    __tablename__ = "parcels"

    id: Mapped[str] = Column(String, primary_key=True, index=True)
    canton: Mapped[str] = Column(String, index=True, nullable=False)
    area_m2: Mapped[float] = Column(Float, nullable=False)
    zoning: Mapped[str] = Column(String, nullable=False)
    is_buildable: Mapped[bool] = Column(Boolean, nullable=False)

    geometry = Column(JSON)
    lon = Column(Float, nullable=True)
    lat = Column(Float, nullable=True)


class ParcelCreate(BaseModel):
    id: str
    canton: str
    area_m2: float
    zoning: str
    is_buildable: bool


class Parcel(ParcelCreate):
    geometry: Optional[Dict[str, Any]] = None
    lon: Optional[float] = None
    lat: Optional[float] = None

    class Config:
        from_attributes = True
