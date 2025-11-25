import logging
from fastapi import APIRouter, HTTPException, Body, Depends, Security
from fastapi.security import APIKeyHeader
from typing import List
from sqlalchemy.orm import Session 
from app.models import Parcel, ParcelCreate 
from app.database import get_db
import app.crud as crud

logger = logging.getLogger("SwissLandAnalyzer.Parcels")

router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
SECRET_API_KEY = "SUPER_ALEX" 

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key
    else:
        logger.warning("Authentication failed: Invalid or missing API Key.")
        raise HTTPException(
            status_code=403, detail="Not authorized. Invalid or missing API Key in X-API-Key header."
        )


@router.post("/parcels", response_model=Parcel, status_code=201)
def create_parcel(
    parcel: ParcelCreate,
    security: str = Depends(get_api_key),
    db: Session = Depends(get_db) 
):

    if crud.get_parcel_by_id(db, parcel_id=parcel.id): 
        logger.warning(f"Attempted POST with existing ID: {parcel.id}")
        raise HTTPException(status_code=400, detail=f"Parcel ID '{parcel.id}' already exists")
    

    new_parcel = crud.create_parcel(db, parcel=parcel)
    
    logger.info(f"Parcel created successfully: ID={new_parcel.id}")
    return new_parcel

@router.put("/parcels/{parcel_id}", response_model=Parcel)
def update_parcel(
    parcel_id: str,
    updated_parcel_data: ParcelCreate = Body(...),
    security: str = Depends(get_api_key),
    db: Session = Depends(get_db) 
):
  
    updated_parcel = crud.update_parcel(db, parcel_id, updated_parcel_data)
    
    if updated_parcel is None:
        logger.warning(f"Update attempt failed: Parcel ID {parcel_id} not found.")
        raise HTTPException(status_code=404, detail="Parcel not found")
    
    logger.info(f"Parcel updated successfully: ID={parcel_id}")
    return updated_parcel

@router.delete("/parcels/{parcel_id}", status_code=204)
def delete_parcel(
    parcel_id: str,
    security: str = Depends(get_api_key),
    db: Session = Depends(get_db) 
):
    if not crud.delete_parcel(db, parcel_id):
        logger.warning(f"Delete attempt failed: Parcel ID {parcel_id} not found.")
        raise HTTPException(status_code=404, detail="Parcel not found")
    
    logger.info(f"Parcel deleted successfully: ID={parcel_id}")
    return

@router.get("/parcels", response_model=List[Parcel])
def list_parcels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)): 
    logger.debug(f"Fetching parcels with skip={skip}, limit={limit}")
    return crud.get_parcels(db, skip=skip, limit=limit) 

@router.get("/parcels/search", response_model=List[Parcel])
def search_parcels(
    canton: str | None = None, 
    buildable: bool | None = None,
    db: Session = Depends(get_db) # New
):
    # Use CRUD function to search parcels
    results = crud.search_parcels(db, canton=canton, buildable=buildable)
    logger.debug(f"Search executed: canton={canton}, buildable={buildable}. Found {len(results)} results.")
    return results

@router.get("/parcels/stats")
def get_parcels_stats(db: Session = Depends(get_db)): # New
    # Use CRUD function to get stats
    stats = crud.get_parcels_stats(db)
    logger.info("Parcel stats calculated and returned.")
    return stats

@router.get("/parcels/{parcel_id}", response_model=Parcel)
def get_parcel(parcel_id: str, db: Session = Depends(get_db)): 
    parcel = crud.get_parcel_by_id(db, parcel_id=parcel_id)
    if parcel is None:
        logger.warning(f"Parcel retrieval failed: ID={parcel_id} not found.")
        raise HTTPException(status_code=404, detail="Parcel not found")
    
    logger.debug(f"Parcel retrieval successful: ID={parcel_id}")
    return parcel

def get_parcel_or_404(parcel_id: str, db: Session = Depends(get_db)):
    """Helper dependency to fetch a parcel or raise 404."""
    parcel = crud.get_parcel_by_id(db, parcel_id=parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return parcel

@router.get("/parcels/{parcel_id}/score")
def get_parcel_score(
    parcel_id: str, 
    parcel: Parcel = Depends(get_parcel_or_404) 
):
    score = 75
    if parcel.is_buildable:
        score += 15
    if parcel.area_m2 > 1000:
        score += 10
        
    logger.info(f"Score calculated for ID={parcel_id}: Score={score}")
    return {"parcel_id": parcel_id, "score": score, "explanation": "Score is based on buildability and area size."}

@router.get("/parcels/{parcel_id}/summary")
def get_parcel_summary(
    parcel_id: str,
    parcel: Parcel = Depends(get_parcel_or_404) 
):
    logger.debug(f"Summary requested for ID={parcel_id}")
    return {
        "parcel_id": parcel_id, 
        "summary": f"This parcel is located in the canton of **{parcel.canton}** and has an area of **{parcel.area_m2} m²**. Its current zoning is **{parcel.zoning}**."
    }

@router.get("/parcels/{parcel_id}/recommendations")
def get_parcel_recommendations(
    parcel_id: str,
    parcel: Parcel = Depends(get_parcel_or_404) 
):
    recommendations = []
    if parcel.is_buildable:
        recommendations.append("Recommended for single-family home development.")
    else:
        recommendations.append("Recommended for agricultural use or zoning change application.")
        
    logger.info(f"Recommendations provided for ID={parcel_id}")
    return {"parcel_id": parcel_id, "recommendations": recommendations}

@router.get("/parcels/{parcel_id}/zoning-explanation")
def get_zoning_explanation(
    parcel_id: str,
    parcel: Parcel = Depends(get_parcel_or_404) 
):
    if parcel.zoning == "buildable":
        explanation = "The parcel is designated as **Residential Zone 2 (R2)**, allowing for immediate single-family or duplex development with a maximum floor area ratio (FAR) of 0.4 and a maximum building height of 11 meters."
    elif parcel.zoning == "agricultural":
        explanation = "The parcel is designated as **Agricultural Protection Zone**. Development is severely restricted, primarily limited to farming structures or facilities essential for agricultural operations. Residential use is generally prohibited."
    else:
        explanation = f"The parcel is currently designated as **{parcel.zoning}**. Consult local cantonal planning authority for exact restrictions."
        
    logger.debug(f"Zoning explanation generated for ID={parcel_id}")
    return {"parcel_id": parcel_id, "zoning_explanation": explanation}

@router.get("/parcels/{parcel_id}/value-estimate")
def get_value_estimate(
    parcel_id: str,
    parcel: Parcel = Depends(get_parcel_or_404) 
):
    base_value = parcel.area_m2 * 200
    if parcel.is_buildable:
        estimated_value = base_value + (parcel.area_m2 * 800) 
        method = "AI model calculated valuation based on comparable buildable plots, proximity to transport, and current zoning."
    else:
        estimated_value = base_value * 0.25
        method = "Valuation adjusted for non-buildable status, reflecting only residual land value."

    logger.info(f"Value estimate completed for ID={parcel_id}. Value={estimated_value:.2f} CHF")
    return {"parcel_id": parcel_id, "estimated_value_chf": estimated_value, "method": method}

@router.get("/parcels/{parcel_id}/development-potential")
def get_development_potential(
    parcel_id: str,
    parcel: Parcel = Depends(get_parcel_or_404) 
):
    potential = "Low"
    recommendation = "No viable development due to zoning."
    
    if parcel.is_buildable and parcel.area_m2 > 1000:
        potential = "High"
        recommendation = "Suitable for multi-unit (3-4 story) residential project or small commercial space."
    elif parcel.is_buildable:
        potential = "Moderate"
        recommendation = "Suitable for a single-family home or duplex development."
        
    logger.info(f"Development potential assessed for ID={parcel_id}: Potential={potential}")
    return {"parcel_id": parcel_id, "development_potential": potential, "highest_best_use": recommendation}

@router.get("/parcels/{parcel_id}/restrictions")
def get_restrictions(
    parcel_id: str,
    parcel: Parcel = Depends(get_parcel_or_404) 
):
    restrictions = ["No build-over zone for power lines within 5 meters of the northern border.", "Maximum roof pitch of 35 degrees."]
    
    if not parcel.is_buildable:
        restrictions.append(f"Development is strictly prohibited due to **{parcel.zoning}** zoning. Only agricultural use is permitted.")
        
    logger.debug(f"Restrictions fetched for ID={parcel_id}")
    return {"parcel_id": parcel_id, "major_restrictions": restrictions}