from fastapi import FastAPI
from app.routers import parcels

app = FastAPI()

app.include_router(parcels.router)

@app.get("/")
def root():
    return {"message": "SwissParcel backend is running"}

@app.get("/status")
def status():
    return {"status": "ok"}
