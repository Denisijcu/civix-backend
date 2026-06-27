from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Al usar ConfigDict, garantizamos compatibilidad total con Pydantic v2
# y la validación nativa de Rust.

class UserCreate(BaseModel):
    id: str
    nombre: str
    email: EmailStr

class UserOut(BaseModel):
    id: str
    nombre: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)

class ProgressOut(BaseModel):
    usuario_id: str
    preguntas_respondidas: int
    respuestas_correctas: int
    probabilidad_aprobacion: float
    nivel_estres_actual: int
    
    model_config = ConfigDict(from_attributes=True)