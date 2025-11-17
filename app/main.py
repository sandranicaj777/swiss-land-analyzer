from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SwissParcel backend is running"}


#fake data
@app.get("/parcels/{parcel_id}")
def get_parcel(parcel_id: str):
    sample_parcel = {
        "id": 1,
        "canton": "FR",
        "municipality": "Exampleville",
        "area_m2": 1234,
        "zoning": "buildable",
        "is_buildable": True,
        "estimated_value_chf": 250_000,
    }
    return sample_parcel

#fake data
@app.get("/status")
def status():
    return {"status": "ok"}

