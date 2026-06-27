import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import progress, interview

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Civix API", version="0.2.0")

# Simple split — no JSON parsing
allowed_origins_str = os.getenv("ALLOW_ORIGINS", "http://localhost:4200")
allowed_origins = [o.strip() for o in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(progress.router)
app.include_router(interview.router)

@app.get("/health")
def health_check():
    return {"status": "online", "service": "Civix-Core"}