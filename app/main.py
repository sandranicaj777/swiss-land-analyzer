from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SwissParcel backend is running"}
