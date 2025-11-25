from fastapi import APIRouter, HTTPException, Body
from typing import List
from app.models import Parcel, ParcelCreate 
from app.data import FAKE_PARCELS

router = APIRouter()

def find_parcel_index(parcel_id: str) -> int:
    """Finds the index of a parcel in FAKE_PARCELS by its ID."""
    for i, parcel in enumerate(FAKE_PARCELS):
        if parcel.id == parcel_id:
            return i
    return -1

@router.post("/parcels", response_model=Parcel, status_code=201)
def create_parcel(parcel: ParcelCreate):
    """
    Creates a new parcel.
    """
    if find_parcel_index(parcel.id) != -1:
        raise HTTPException(status_code=400, detail=f"Parcel ID '{parcel.id}' already exists")
    
    new_parcel = Parcel(**parcel.model_dump())
    
    FAKE_PARCELS.append(new_parcel)
    
    return new_parcel

@router.put("/parcels/{parcel_id}", response_model=Parcel)
def update_parcel(parcel_id: str, updated_parcel_data: ParcelCreate = Body(...)):
    """
    Updates an existing parcel by ID.
    """
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")

    update_data = updated_parcel_data.dict(exclude={'id'}) 
    
    updated_parcel = Parcel(id=parcel_id, **update_data) 
    
    FAKE_PARCELS[index] = updated_parcel
    
    return updated_parcel

@router.delete("/parcels/{parcel_id}", status_code=204)
def delete_parcel(parcel_id: str):
    """
    Deletes a parcel by ID.
    """
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
    
    del FAKE_PARCELS[index]
    
    return

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

