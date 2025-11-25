import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.routers import parcels
from app.database import create_db_tables, engine 
from app.models import Base 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SwissLandAnalyzer")

create_db_tables()

app = FastAPI(
    title="Swiss Land Analyzer API",
    description="Backend API for Swiss Land Parcel Analysis (Database Version)",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080", 
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              
    allow_credentials=True,             
    allow_methods=["*"],                
    allow_headers=["*"],                
)

app.include_router(parcels.router, tags=["Parcels"])

@app.get("/")
def root():
    """Simple root endpoint to confirm the API is running."""
    logger.info("Root endpoint accessed.")
    return {"message": "SwissParcel backend is running (v1.0.0, Database enabled)"}

@app.get("/status")
def status():
    """Simple status check endpoint."""
    logger.debug("Status endpoint accessed.")
    return {"status": "ok"}