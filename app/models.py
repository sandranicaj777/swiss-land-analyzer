from pydantic import BaseModel
from typing import Optional

class Parcel(BaseModel):
    id: str
    canton: str
    municipality: str
    area_m2: float
    zoning: str
    is_buildable: bool
    estimated_value_chf: Optional[float] = None
