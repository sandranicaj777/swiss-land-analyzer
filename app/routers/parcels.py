from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Parcel
from app.data import FAKE_PARCELS

router = APIRouter()

@router.get("/parcels", response_model=List[Parcel])
def list_parcels():
    return FAKE_PARCELS

@router.get("/parcels/search", response_model=List[Parcel])
def search_parcels(canton: str | None = None, buildable: bool | None = None):
    results = FAKE_PARCELS
    if canton:
        results = [p for p in results if p.canton.lower() == canton.lower()]
    if buildable is not None:
        results = [p for p in results if p.is_buildable == buildable]
    return results


@router.get("/parcels/{parcel_id}", response_model=Parcel)
def get_parcel(parcel_id: str):
    for parcel in FAKE_PARCELS:
        if parcel.id == parcel_id:
            return parcel
    raise HTTPException(status_code=404, detail="Parcel not found")

