import geopandas as gpd
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models import ParcelORM

FILE_PATH = "app/data/fribourg_av.gpkg"
LAYER = "lcsf"
BATCH_SIZE = 1000

print("Loading Fribourg cadastral parcels...")
gdf = gpd.read_file(FILE_PATH, layer=LAYER)

gdf = gdf.to_crs(epsg=2056)
gdf_wgs84 = gdf.to_crs(epsg=4326)

NON_BUILDABLE_GENRES = {
    "autre_boisee",
    "champ_pre_paturage",
    "autre_boisee_dense",
    "eau",
    "rocher",
}

db = SessionLocal()
batch = []
count = 0

for idx, row in gdf.iterrows():
    geom_m = row.geometry
    if geom_m is None:
        continue

    geom_wgs = gdf_wgs84.loc[idx].geometry
    genre = row.get("Genre", "unknown")

    parcel = ParcelORM(
        id=f"FR-{row['NoOFS']}-{idx}",
        canton="FR",
        area_m2=float(geom_m.area),
        zoning=genre,
        is_buildable=genre not in NON_BUILDABLE_GENRES,
        geometry=geom_wgs.__geo_interface__,
        lon=geom_wgs.centroid.x,
        lat=geom_wgs.centroid.y,
    )

    batch.append(parcel)

    if len(batch) >= BATCH_SIZE:
        db.bulk_save_objects(batch)
        db.commit()
        batch.clear()
        count += BATCH_SIZE
        print(f"Inserted {count} parcels...")

# final flush
if batch:
    db.bulk_save_objects(batch)
    db.commit()
    count += len(batch)

db.close()
print(f"✅ Imported {count} Fribourg parcels into Neon")
