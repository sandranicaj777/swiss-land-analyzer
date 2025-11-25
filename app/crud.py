from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Dict, Any
from app.models import ParcelORM, ParcelCreate


def get_parcels(db: Session, skip: int = 0, limit: int = 10) -> List[ParcelORM]:
    """Retrieves a list of parcels with pagination."""
    return db.scalars(select(ParcelORM).offset(skip).limit(limit)).all()

def get_parcel_by_id(db: Session, parcel_id: str) -> ParcelORM | None:
    """Retrieves a single parcel by its ID."""
    return db.scalar(select(ParcelORM).where(ParcelORM.id == parcel_id))

def search_parcels(db: Session, canton: str | None, buildable: bool | None) -> List[ParcelORM]:
    """Searches parcels based on optional filters."""
    stmt = select(ParcelORM)
    if canton:
        stmt = stmt.where(func.lower(ParcelORM.canton) == canton.lower())
    if buildable is not None:
        stmt = stmt.where(ParcelORM.is_buildable == buildable)
        
    return db.scalars(stmt).all()

def get_parcels_stats(db: Session) -> Dict[str, Any]:
    """Calculates and returns statistics on all parcels."""
    total_parcels = db.query(ParcelORM).count()
    if total_parcels == 0:
        return {"total_parcels": 0, "buildable_percentage": "0.00%", "average_area_m2": "0.00"}

    buildable_count = db.query(ParcelORM).filter(ParcelORM.is_buildable == True).count()
    average_area_result = db.query(func.avg(ParcelORM.area_m2)).scalar()

    return {
        "total_parcels": total_parcels,
        "buildable_percentage": f"{(buildable_count / total_parcels) * 100:.2f}%",
        "average_area_m2": f"{average_area_result:.2f}"
    }

def create_parcel(db: Session, parcel: ParcelCreate) -> ParcelORM:
    """Creates a new parcel in the database."""
    db_parcel = ParcelORM(**parcel.model_dump())
    db.add(db_parcel)
    db.commit()
    db.refresh(db_parcel)
    return db_parcel


def update_parcel(db: Session, parcel_id: str, updated_data: ParcelCreate) -> ParcelORM | None:
    """Updates an existing parcel."""
    db_parcel = db.get(ParcelORM, parcel_id)
    if not db_parcel:
        return None

    for key, value in updated_data.model_dump(exclude={'id'}).items():
        setattr(db_parcel, key, value)

    db.commit()
    db.refresh(db_parcel)
    return db_parcel


def delete_parcel(db: Session, parcel_id: str) -> bool:
    """Deletes a parcel by ID."""
    db_parcel = db.get(ParcelORM, parcel_id)
    if not db_parcel:
        return False
    
    db.delete(db_parcel)
    db.commit()
    return True