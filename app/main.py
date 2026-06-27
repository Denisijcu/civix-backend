import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import progress, interview

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Civix API", version="0.2.0")

# CORS Hardening: Permite flexibilidad sin trailing slashes
origins = [
    "https://vertex-civix.netlify.app", 
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(progress.router)
app.include_router(interview.router)

@app.get("/health") # Usar /health es mejor práctica para monitoreo en Railway
def health_check():
    return {"status": "online", "service": "Civix-Core"}