from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, conint

# === Estudiante Básico ===


class EstudianteOut(BaseModel):
    estudiante_id: int
    nombres: str
    ap_paterno: str
    ap_materno: str
    ci: str
    telefono: Optional[str] = None

    class Config:
        orm_mode = True


class EstudianteConMatriculaOut(BaseModel):
    matricula_id: int
    estudiante_id: int
    nombres: str
    ap_paterno: str
    ap_materno: str
    ci: str
    telefono: Optional[str] = None
    nota_final: Optional[float] = None  # ⬅️ nueva
    estado: Optional[str] = None      # ⬅️ nueva

    class Config:
        orm_mode = True


class EstudianteConNotaOut(BaseModel):
    matricula_id: int
    estudiante_id: int
    nombres: str
    ap_paterno: str
    ap_materno: str
    ci: str
    telefono: Optional[str] = None
    nota_final: Optional[float] = None
    estado: Optional[str] = None

    class Config:
        orm_mode = True

# === Horario con datos básicos ===


class HorarioBase(BaseModel):
    horario_id: int
    curso_id: int
    aula_id: int
    gestion_id: int
    profesor_id: int
    activo: bool

    class Config:
        orm_mode = True


# === Horario con estudiantes inscritos ===

class HorarioConEstudiantesOut(BaseModel):
    horario_id: int
    curso_id: int
    aula_id: int
    profesor_id: int
    gestion_id: int
    activo: bool
    estudiantes: List[EstudianteConMatriculaOut]  # 🔁 aquí cambió

    class Config:
        orm_mode = True


class ActualizarNota(BaseModel):
    nota_final: conint(ge=1, le=100)  # Solo acepta valores de 1 a 100
