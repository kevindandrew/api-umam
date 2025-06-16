# schemas/estudiante.py
from pydantic import Field, BaseModel
from typing import List, Optional
from datetime import date, datetime
from enum import Enum


# === Datos familiares ===

class TipoFamiliar(str, Enum):
    referencia = "referencia"
    conviviente = "conviviente"
    emergencia = "emergencia"


# Datos familiares con campos obligatorios
class DatosFamiliarCreate(BaseModel):
    tipo: TipoFamiliar
    ap_paterno: str = Field(..., min_length=1)  # Obligatorio
    ap_materno: str = Field(..., min_length=1)  # Obligatorio
    nombres: str = Field(..., min_length=1)     # Obligatorio
    parentesco: str = Field(..., min_length=1)  # Obligatorio
    telefono: str = Field(..., min_length=1)    # Obligatorio
    direccion: str = Field(..., min_length=1)   # Obligatorio
    relacion: str = Field(..., min_length=1)    # Obligatorio


class DatosFamiliarOut(DatosFamiliarCreate):
    familiar_id: int

    class Config:
        orm_mode = True


# === Datos académicos ===
# Datos académicos con campo obligatorio
class DatosAcademicoCreate(BaseModel):
    grado_institucion: str = Field(..., min_length=1)  # Obligatorio
    anios_servicio: Optional[int] = None
    ultimo_cargo: Optional[str] = None
    otras_habilidades: Optional[str] = None


class DatosAcademicoOut(DatosAcademicoCreate):
    academico_id: int

    class Config:
        orm_mode = True


# === Datos médicos ===
# Datos médicos con campos obligatorios
class DatosMedicoCreate(BaseModel):
    sistema_salud: str = Field(..., min_length=1)       # Obligatorio
    tratamiento_especifico: Optional[str] = None  # Cambiado a Optional
    tuvo_covid: bool                                   # Obligatorio
    frecuencia_medico: Optional[str] = None
    enfermedad_base: Optional[str] = None
    alergias: Optional[str] = None


class DatosMedicoOut(DatosMedicoCreate):
    medico_id: int

    class Config:
        orm_mode = True


# === Estudiante ===
# Estudiante con campos obligatorios
class EstudianteBase(BaseModel):
    nombres: str = Field(..., min_length=1)
    ap_paterno: str = Field(..., min_length=1)
    ap_materno: str = Field(..., min_length=1)
    ci: str = Field(..., min_length=1)
    telefono: str = Field(..., min_length=1)           # Obligatorio
    fecha_nacimiento: date                             # Obligatorio
    genero: str = Field(..., min_length=1)             # Obligatorio
    lugar_nacimiento: str = Field(..., min_length=1)   # Obligatorio
    estado_civil: str = Field(..., min_length=1)       # Obligatorio
    direccion: str = Field(..., min_length=1)          # Obligatorio
    como_se_entero: str = Field(..., min_length=1)     # Obligatorio


class EstudianteCreate(EstudianteBase):
    datos_familiares: Optional[List[DatosFamiliarCreate]] = []
    datos_academicos: Optional[List[DatosAcademicoCreate]] = []
    datos_medicos: Optional[List[DatosMedicoCreate]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "nombres": "Kevin",
                "ap_paterno": "Rojas",
                "ap_materno": "Flores",
                "ci": "12345678",
                "telefono": "71234567",
                "fecha_nacimiento": "2003-09-20",
                "genero": "Masculino",
                "lugar_nacimiento": "Cochabamba",
                "estado_civil": "Soltero",
                "direccion": "Av. Blanco Galindo",
                "como_se_entero": "Facebook",
                "datos_familiares": [
                    {
                        "tipo": "referencia",
                        "ap_paterno": "Rojas",
                        "ap_materno": "Lopez",
                        "nombres": "Juan",
                        "parentesco": "Padre",
                        "telefono": "78965412",
                        "direccion": "Zona Norte",
                        "relacion": "Buena"
                    }
                ],
                "datos_academicos": [
                    {
                        "grado_institucion": "Colegio Nacional",
                        "anios_servicio": 4,
                        "ultimo_cargo": "Delegado",
                        "otras_habilidades": "Inglés, informática"
                    }
                ],
                "datos_medicos": [
                    {
                        "sistema_salud": "Caja Nacional",
                        "frecuencia_medico": "Mensual",
                        "enfermedad_base": "Ninguna",
                        "alergias": "Polvo",
                        "tratamiento_especifico": "Antialérgicos",
                        "tuvo_covid": False
                    }
                ]
            }
        }


class EstudianteOut(EstudianteBase):
    estudiante_id: int
    fecha_registro: datetime
    datos_familiares: List[DatosFamiliarOut] = []
    datos_academicos: List[DatosAcademicoOut] = []
    datos_medicos: List[DatosMedicoOut] = []

    class Config:
        orm_mode = True
