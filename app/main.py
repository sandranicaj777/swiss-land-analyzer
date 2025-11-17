from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Parcel(BaseModel):
    id: str
    canton: str
    municipality: str
    area_m2: float
    zoning: str
    is_buildable: bool
    estimated_value_chf: Optional[float] = None


FAKE_PARCELS = [
    Parcel(
        id="12345",
        canton="FR",
        municipality="Exampleville",
        area_m2=1200,
        zoning="buildable",
        is_buildable=True,
        estimated_value_chf=250_000,
    ),
    Parcel(
        id="67890",
        canton="FR",
        municipality="Sampletown",
        area_m2=800,
        zoning="agricultural",
        is_buildable=False,
        estimated_value_chf=None,
    ),
]


@app.get("/")
def root():
    return {"message": "SwissParcel backend is running"}


@app.get("/status")
def status():
    return {"status": "ok"}


@app.get("/parcels", response_model=List[Parcel])
def list_parcels():
    return FAKE_PARCELS


@app.get("/parcels/{parcel_id}", response_model=Parcel)
def get_parcel(parcel_id: str):
    for parcel in FAKE_PARCELS:
        if parcel.id == parcel_id:
            return parcel
    return {"error": "Parcel not found"}
