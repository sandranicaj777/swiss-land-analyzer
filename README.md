# 🇨🇭 Swiss Land Analyzer API
 
A FastAPI backend for analyzing Swiss land parcels — providing zoning data, AI-generated summaries, development potential assessments, value estimates, and GeoJSON export.
 
---
 
## Features
 
- Full CRUD for land parcels (secured with API key)
- Parcel search with filters (canton, zoning, area, buildability)
- Aggregate stats endpoint
- GeoJSON export for map rendering
- Per-parcel endpoints: score, value estimate, zoning explanation, restrictions, recommendations
- AI-powered summary and development potential via local [Ollama](https://ollama.com/) (llama3.2:3b)
---
 
## Project Structure
 
```
app/
├── main.py          # FastAPI app setup, CORS, router registration
├── database.py      # SQLAlchemy engine, session, Base
├── models.py        # ORM model (ParcelORM) + Pydantic schemas (Parcel, ParcelCreate)
├── crud.py          # Database operations (create, read, update, delete, search, stats)
├── data.py          # Sample/fake parcel data for testing
├── routers/
│   └── parcels.py   # All parcel API routes
└── ai/
    └── parcel_ai.py # Ollama-based AI text generation with output filtering
```
 
---
 
## Requirements
 
- Python 3.11+
- PostgreSQL (or any SQLAlchemy-compatible DB)
- [Ollama](https://ollama.com/) running locally with `llama3.2:3b` pulled
Install dependencies:
 
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv requests
```
 
---
 
## Configuration
 
Create a `.env` file in the project root:
 
```env
DATABASE_URL=postgresql://user:password@localhost:5432/swissland
```
 
---
 
## Running the API
 
```bash
uvicorn app.main:app --reload
```
 
The API will be available at `http://localhost:8000`. Interactive docs at `/docs`.
 
---
 
## Authentication
 
Write endpoints (POST, PUT, DELETE) require an API key in the request header:
 
```
X-API-Key: SUPER_ALEX
```
 
Read endpoints are public.
 
---
 
## API Endpoints
 
### Core CRUD
 
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/parcels` | No | List parcels (paginated) |
| `GET` | `/parcels/{id}` | No | Get a single parcel |
| `POST` | `/parcels` | Yes | Create a parcel |
| `PUT` | `/parcels/{id}` | Yes | Update a parcel |
| `DELETE` | `/parcels/{id}` | Yes | Delete a parcel |
 
### Search & Stats
 
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/parcels/search` | Filter by canton, zoning, buildability, area range |
| `GET` | `/parcels/stats` | Total count, buildable %, average area |
| `GET` | `/parcels/geojson` | GeoJSON FeatureCollection (up to 5000 parcels) |
 
### Per-Parcel Analysis
 
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/parcels/{id}/score` | Numeric score based on buildability and area |
| `GET` | `/parcels/{id}/summary` | AI-generated parcel summary (Ollama) |
| `GET` | `/parcels/{id}/value-estimate` | Estimated value in CHF |
| `GET` | `/parcels/{id}/zoning-explanation` | Human-readable zoning description |
| `GET` | `/parcels/{id}/development-potential` | AI-assessed development potential |
| `GET` | `/parcels/{id}/recommendations` | Use recommendations based on zoning |
| `GET` | `/parcels/{id}/restrictions` | Known build restrictions |
 
### Search Query Parameters
 
| Param | Type | Description |
|-------|------|-------------|
| `canton` | string | Filter by canton code (e.g. `ZH`) |
| `buildable` | bool | Filter by buildable status |
| `min_area` | float | Minimum area in m² |
| `max_area` | float | Maximum area in m² |
| `zoning` | string | Partial match on zoning type |
| `limit` | int | Max results (default 50) |
 
---
 
## AI Integration
 
AI features use a locally running Ollama instance. Make sure it is running before starting the server:
 
```bash
ollama serve
ollama pull llama3.2:3b
```
 
The AI module (`parcel_ai.py`) includes an output filter (`_clean_ai_text`) that strips common LLM artifacts — self-references, first-person phrasing, and overly long responses — to ensure clean, platform-appropriate copy. If the AI call fails or produces unusable output, a deterministic fallback is returned.
 
Ollama is expected at: `http://localhost:11434`
 
---
 
## Parcel Data Model
 
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | Yes | Unique parcel identifier |
| `canton` | string | Yes | Swiss canton code |
| `area_m2` | float | Yes | Area in square metres |
| `zoning` | string | Yes | e.g. `buildable`, `agricultural` |
| `is_buildable` | bool | Yes | Derived from zoning/regulations |
| `geometry` | JSON | No | GeoJSON geometry object |
| `lon` / `lat` | float | No | Centroid coordinates |
 
---
 

