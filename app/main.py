import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import progress, interview

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Civix API", version="0.2.0")

# CORS Hardening: Carga dinámica desde variable de entorno
# Asegúrate de que el valor en Railway sea: ["https://vertex-civix.netlify.app", "http://localhost:4200"]
allowed_origins_str = os.getenv("ALLOW_ORIGINS", '["http://localhost:4200"]')

try:
    allowed_origins = json.loads(allowed_origins_str)
except json.JSONDecodeError:
    allowed_origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(progress.router)
app.include_router(interview.router)

@app.get("/health")
def health_check():
    return {"status": "online", "service": "Civix-Core"}