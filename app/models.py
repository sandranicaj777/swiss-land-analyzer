from pydantic import BaseModel, Field
from typing import Optional

class Parcel(BaseModel):
    id: str = Field(..., description="Unique ID of the parcel, e.g., '12345'")
    canton: str
    municipality: str
    area_m2: float = Field(..., gt=0, description="Area in square meters.")
    zoning: str
    is_buildable: bool
    estimated_value_chf: Optional[float] = None

class ParcelCreate(BaseModel):
    id: str = Field(..., description="Unique ID for the new parcel.")
    canton: str
    municipality: str
    area_m2: float = Field(..., gt=0)
    zoning: str
    is_buildable: bool
    estimated_value_chf: Optional[float] = None