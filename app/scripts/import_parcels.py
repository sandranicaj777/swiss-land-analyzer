import geopandas as gpd
from app.database import SessionLocal
from app.models import ParcelORM

gdf = gpd.read_file("fribourg_parcels.geojson")

db = SessionLocal()

for _, row in gdf.iterrows():
    centroid = row.geometry.centroid

    parcel = ParcelORM(
        id=row["parcel_id"],
        canton="FR",
        area_m2=row["area"],
        zoning=row["zone"],
        is_buildable=row["zone"] == "buildable",
        lon=centroid.x,
        lat=centroid.y,
    )
    db.add(parcel)

db.commit()
