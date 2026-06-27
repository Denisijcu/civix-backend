
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/progress", tags=["Progress"])

@router.get("/{user_id}", response_model=schemas.ProgressOut)
def get_user_progress(user_id: str, db: Session = Depends(get_db)):
    # Busca el progreso. Si no existe, lanza error 404
    progress = db.query(models.UserProgress).filter(models.UserProgress.usuario_id == user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o sin progreso aún.")
    return progress