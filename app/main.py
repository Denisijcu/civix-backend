from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import progress
from app.routers import interview  # <-- NUEVO

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Civix API", version="0.2.0")

# CORS
origins = ["http://localhost:4200", "http://127.0.0.1:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(progress.router)
app.include_router(interview.router) # <-- NUEVO

@app.get("/")
def read_root():
    return {"message": "Civix API with Claude AI running"}