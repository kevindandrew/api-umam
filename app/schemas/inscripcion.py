from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --------- BASE ---------
class MatriculaBase(BaseModel):
    estudiante_id: int
    horario_id: int
    gestion_id: int


# --------- CREAR ---------
class MatriculaCreate(MatriculaBase):
    pass


# --------- ACTUALIZAR ---------
class MatriculaUpdate(BaseModel):
    nota_final: Optional[float] = None
    estado: Optional[str] = None


# --------- RESPUESTA ---------
class MatriculaOut(MatriculaBase):
    matricula_id: int
    fecha_matricula: datetime
    nota_final: Optional[float]
    estado: str

    class Config:
        orm_mode = True
