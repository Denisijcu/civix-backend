
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    progreso = relationship("UserProgress", back_populates="usuario", uselist=False)

class UserProgress(Base):
    __tablename__ = "user_progress"

    usuario_id = Column(String, ForeignKey("users.id"), primary_key=True)
    preguntas_respondidas = Column(Integer, default=0)
    respuestas_correctas = Column(Integer, default=0)
    probabilidad_aprobacion = Column(Float, default=0.0)
    nivel_estres_actual = Column(Integer, default=1) # 1 al 10 para la gamificación
    fecha_ultimo_acceso = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("User", back_populates="progreso")