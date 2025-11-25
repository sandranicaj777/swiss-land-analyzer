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

@router.get("/parcels/stats")
def get_parcels_stats():
    """Returns aggregated statistics about all parcels."""
    total_parcels = len(FAKE_PARCELS)
    if total_parcels == 0:
        return {"total_parcels": 0, "buildable_percentage": "0.00%", "average_area_m2": "0.00"}
        
    buildable_count = sum(1 for p in FAKE_PARCELS if p.is_buildable)
    average_area = sum(p.area_m2 for p in FAKE_PARCELS) / total_parcels 
    
    return {
        "total_parcels": total_parcels,
        "buildable_percentage": f"{(buildable_count / total_parcels) * 100:.2f}%",
        "average_area_m2": f"{average_area:.2f}"
    }




@router.get("/parcels/{parcel_id}", response_model=Parcel)
def get_parcel(parcel_id: str):
    for parcel in FAKE_PARCELS:
        if parcel.id == parcel_id:
            return parcel
    raise HTTPException(status_code=404, detail="Parcel not found")


@router.get("/parcels/{parcel_id}/score")
def get_parcel_score(parcel_id: str):
    """Calculates and returns a mock development score for a parcel."""
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
    
    parcel = FAKE_PARCELS[index]
    score = 75
    if parcel.is_buildable:
        score += 15
    if parcel.area_m2 > 1000:
        score += 10
        
    return {"parcel_id": parcel_id, "score": score, "explanation": "Score is based on buildability and area size."}

@router.get("/parcels/{parcel_id}/summary")
def get_parcel_summary(parcel_id: str):
    """Returns a brief, generated summary of a parcel."""
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
        
    parcel = FAKE_PARCELS[index]
    return {
        "parcel_id": parcel_id, 
        "summary": f"This parcel is located in the canton of **{parcel.canton}** and has an area of **{parcel.area_m2} m²**. Its current zoning is **{parcel.zoning}**."
    }

@router.get("/parcels/{parcel_id}/recommendations")
def get_parcel_recommendations(parcel_id: str):
    """Provides mock recommendations based on parcel attributes."""
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
        
    parcel = FAKE_PARCELS[index]
    recommendations = []
    if parcel.is_buildable:
        recommendations.append("Recommended for single-family home development.")
    else:
        recommendations.append("Recommended for agricultural use or zoning change application.")
        
    return {"parcel_id": parcel_id, "recommendations": recommendations}

