import geopandas as gpd
from app.database import SessionLocal
from app.models import ParcelORM

FILE_PATH = "app/data/fribourg_av.gpkg"
LAYER = "lcsf"

print("Loading Fribourg cadastral parcels (layer=lcsf)...")
gdf = gpd.read_file(FILE_PATH, layer=LAYER)

print("Original CRS:", gdf.crs)
print("Total parcels:", len(gdf))

gdf_meters = gdf.to_crs(epsg=2056)


gdf_wgs84 = gdf_meters.to_crs(epsg=4326)

NON_BUILDABLE_GENRES = {
    "autre_boisee",
    "champ_pre_paturage",
    "autre_boisee_dense",
    "eau",
    "rocher",
}

db = SessionLocal()
count = 0

for idx, row in gdf_meters.iterrows():
    geom_m = row.geometry
    if geom_m is None:
        continue

    area_m2 = float(geom_m.area)

    geom_wgs = gdf_wgs84.loc[idx].geometry

    genre = row.get("Genre", "unknown")
    is_buildable = genre not in NON_BUILDABLE_GENRES

    parcel_id = f"FR-{row['NoOFS']}-{idx}"

    parcel = ParcelORM(
        id=parcel_id,
        canton="FR",
        area_m2=area_m2,
        zoning=genre,
        is_buildable=is_buildable,
        geometry=geom_wgs.__geo_interface__,
        lon=geom_wgs.centroid.x,
        lat=geom_wgs.centroid.y,
    )

    db.add(parcel)
    count += 1

db.commit()
db.close()

print(f"Imported {count} Fribourg parcels with REAL area & zoning")
