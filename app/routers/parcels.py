from fastapi import APIRouter, HTTPException, Body, Depends, Security
from fastapi.security import APIKeyHeader
from typing import List
from app.models import Parcel, ParcelCreate 
from app.data import FAKE_PARCELS

router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
SECRET_API_KEY = "SUPER_SECRET_TOKEN" 

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=403, detail="Not authorized. Invalid or missing API Key in X-API-Key header."
        )

def find_parcel_index(parcel_id: str) -> int:
    for i, parcel in enumerate(FAKE_PARCELS):
        if parcel.id == parcel_id:
            return i
    return -1

@router.post("/parcels", response_model=Parcel, status_code=201)
def create_parcel(
    parcel: ParcelCreate,
    security: str = Depends(get_api_key)
):
    if find_parcel_index(parcel.id) != -1:
        raise HTTPException(status_code=400, detail=f"Parcel ID '{parcel.id}' already exists")
    
    new_parcel = Parcel(**parcel.model_dump())
    
    FAKE_PARCELS.append(new_parcel)
    
    return new_parcel

@router.put("/parcels/{parcel_id}", response_model=Parcel)
def update_parcel(
    parcel_id: str,
    updated_parcel_data: ParcelCreate = Body(...),
    security: str = Depends(get_api_key)
):
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")

    update_data = updated_parcel_data.dict(exclude={'id'}) 
    
    updated_parcel = Parcel(id=parcel_id, **update_data) 
    
    FAKE_PARCELS[index] = updated_parcel
    
    return updated_parcel

@router.delete("/parcels/{parcel_id}", status_code=204)
def delete_parcel(
    parcel_id: str,
    security: str = Depends(get_api_key)
):
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
    
    del FAKE_PARCELS[index]
    
    return

@router.get("/parcels", response_model=List[Parcel])
def list_parcels(skip: int = 0, limit: int = 10): 
    return FAKE_PARCELS[skip : skip + limit] 

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

@router.get("/parcels/{parcel_id}/zoning-explanation")
def get_zoning_explanation(parcel_id: str):
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
        
    parcel = FAKE_PARCELS[index]
    if parcel.zoning == "buildable":
        explanation = "The parcel is designated as **Residential Zone 2 (R2)**, allowing for immediate single-family or duplex development with a maximum floor area ratio (FAR) of 0.4 and a maximum building height of 11 meters."
    elif parcel.zoning == "agricultural":
        explanation = "The parcel is designated as **Agricultural Protection Zone**. Development is severely restricted, primarily limited to farming structures or facilities essential for agricultural operations. Residential use is generally prohibited."
    else:
        explanation = f"The parcel is currently designated as **{parcel.zoning}**. Consult local cantonal planning authority for exact restrictions."
        
    return {"parcel_id": parcel_id, "zoning_explanation": explanation}

@router.get("/parcels/{parcel_id}/value-estimate")
def get_value_estimate(parcel_id: str):
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
        
    parcel = FAKE_PARCELS[index]
    
    base_value = parcel.area_m2 * 200
    if parcel.is_buildable:
        estimated_value = base_value + (parcel.area_m2 * 800) 
        method = "AI model calculated valuation based on comparable buildable plots, proximity to transport, and current zoning."
    else:
        estimated_value = base_value * 0.25
        method = "Valuation adjusted for non-buildable status, reflecting only residual land value."

    return {"parcel_id": parcel_id, "estimated_value_chf": estimated_value, "method": method}

@router.get("/parcels/{parcel_id}/development-potential")
def get_development_potential(parcel_id: str):
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
        
    parcel = FAKE_PARCELS[index]
    potential = "Low"
    recommendation = "No viable development due to zoning."
    
    if parcel.is_buildable and parcel.area_m2 > 1000:
        potential = "High"
        recommendation = "Suitable for multi-unit (3-4 story) residential project or small commercial space."
    elif parcel.is_buildable:
        potential = "Moderate"
        recommendation = "Suitable for a single-family home or duplex development."
        
    return {"parcel_id": parcel_id, "development_potential": potential, "highest_best_use": recommendation}

@router.get("/parcels/{parcel_id}/restrictions")
def get_restrictions(parcel_id: str):
    index = find_parcel_index(parcel_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Parcel not found")
        
    parcel = FAKE_PARCELS[index]
    restrictions = ["No build-over zone for power lines within 5 meters of the northern border.", "Maximum roof pitch of 35 degrees."]
    
    if not parcel.is_buildable:
        restrictions.append(f"Development is strictly prohibited due to **{parcel.zoning}** zoning. Only agricultural use is permitted.")
        
    return {"parcel_id": parcel_id, "major_restrictions": restrictions}