# schemas/estudiante.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from enum import Enum


# === Datos familiares ===

class TipoFamiliar(str, Enum):
    referencia = "referencia"
    conviviente = "conviviente"
    emergencia = "emergencia"


class DatosFamiliarCreate(BaseModel):
    tipo: TipoFamiliar  # ← Ahora valida automáticamente los valores
    ap_paterno: Optional[str]
    ap_materno: Optional[str]
    nombres: Optional[str]
    parentesco: Optional[str]
    telefono: Optional[str]
    direccion: Optional[str]
    relacion: Optional[str]


class DatosFamiliarOut(DatosFamiliarCreate):
    familiar_id: int

    class Config:
        orm_mode = True


# === Datos académicos ===
class DatosAcademicoCreate(BaseModel):
    grado_institucion: Optional[str]
    anios_servicio: Optional[int]
    ultimo_cargo: Optional[str]
    otras_habilidades: Optional[str]


class DatosAcademicoOut(DatosAcademicoCreate):
    academico_id: int

    class Config:
        orm_mode = True


# === Datos médicos ===
class DatosMedicoCreate(BaseModel):
    sistema_salud: Optional[str]
    frecuencia_medico: Optional[str]
    enfermedad_base: Optional[str]
    alergias: Optional[str]
    tratamiento_especifico: Optional[str]
    tuvo_covid: Optional[bool]


class DatosMedicoOut(DatosMedicoCreate):
    medico_id: int

    class Config:
        orm_mode = True


# === Estudiante ===
class EstudianteBase(BaseModel):
    nombres: str
    ap_paterno: str
    ap_materno: str
    ci: str
    telefono: Optional[str]
    fecha_nacimiento: Optional[date]
    genero: Optional[str]
    lugar_nacimiento: Optional[str]
    estado_civil: Optional[str]
    direccion: Optional[str]
    como_se_entero: Optional[str]


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
