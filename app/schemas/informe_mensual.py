from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InformeMensualCreate(BaseModel):
    carrera: str
    universidad: str
    mes: int = Field(..., ge=1, le=12)
    anio: int = Field(..., ge=2020)
    actividades_realizadas: str
    como_se_realizaron: str
    resultados_obtenidos: str
    relacion_alcaldia: str
    medios_otorgados_alcaldia: str


class InformeMensualUpdate(BaseModel):
    carrera: Optional[str] = None
    universidad: Optional[str] = None
    mes: Optional[int] = Field(None, ge=1, le=12)
    anio: Optional[int] = Field(None, ge=2020)
    actividades_realizadas: Optional[str] = None
    como_se_realizaron: Optional[str] = None
    resultados_obtenidos: Optional[str] = None
    relacion_alcaldia: Optional[str] = None
    medios_otorgados_alcaldia: Optional[str] = None


class InformeMensualOut(BaseModel):
    informe_id: int
    usuario_id: int
    nombre_facilitador: str
    carrera: str
    universidad: str
    mes: int
    anio: int
    actividades_realizadas: str
    como_se_realizaron: str
    resultados_obtenidos: str
    relacion_alcaldia: str
    medios_otorgados_alcaldia: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
