from app.models import Parcel

FAKE_PARCELS = [
    Parcel(
        id="12345",
        canton="FR",
        municipality="Exampleville",
        area_m2=1200,
        zoning="buildable",
        is_buildable=True,
        estimated_value_chf=250_000,
    ),
    Parcel(
        id="67890",
        canton="FR",
        municipality="Sampletown",
        area_m2=800,
        zoning="agricultural",
        is_buildable=False,
        estimated_value_chf=None,
    ),
]
