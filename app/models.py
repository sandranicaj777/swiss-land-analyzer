from pydantic import BaseModel
from sqlalchemy import Column, String, Float, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped
from app.database import Base 

class ParcelORM(Base):
    """
    Represents the 'parcels' table in the database.
    """
    __tablename__ = "parcels"
    
    id: Mapped[str] = Column(String, primary_key=True, index=True)
    
    canton: Mapped[str] = Column(String, index=True, nullable=False)
    area_m2: Mapped[float] = Column(Float, nullable=False)
    zoning: Mapped[str] = Column(String, nullable=False)
    is_buildable: Mapped[bool] = Column(Boolean, nullable=False)
    
class ParcelCreate(BaseModel):
    id: str
    canton: str
    area_m2: float
    zoning: str
    is_buildable: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "2222-A",
                "canton": "ZH",
                "area_m2": 500.5,
                "zoning": "buildable",
                "is_buildable": True
            }
        }

class Parcel(ParcelCreate):
    class Config:
        from_attributes = True 