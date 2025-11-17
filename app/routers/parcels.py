from fastapi import APIRouter
from typing import List
from app.models import Parcel
from app.data import FAKE_PARCELS

router = APIRouter()

@router.get("/parcels", response_model=List[Parcel])
def list_parcels():
    return FAKE_PARCELS

@router.get("/parcels/{parcel_id}", response_model=Parcel)
def get_parcel(parcel_id: str):
    for parcel in FAKE_PARCELS:
        if parcel.id == parcel_id:
            return parcel
    return {"error": "Parcel not found"}
