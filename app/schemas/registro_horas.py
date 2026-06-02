from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class TipoServicio(str, Enum):
    clases = "clases"
    creacion_material = "creacion_material"
    asistencia_eventos = "asistencia_eventos"


class RegistroHorasCreate(BaseModel):
    tipo_servicio: TipoServicio
    observaciones: Optional[str] = None
    sucursal_id: Optional[int] = None


class RegistroHorasAdminCreate(BaseModel):
    tipo_servicio: TipoServicio
    hora_entrada: datetime
    hora_salida: datetime
    observaciones: Optional[str] = None
    sucursal_id: Optional[int] = None


class RegistroHorasOut(BaseModel):
    registro_id: int
    usuario_id: int
    nombre_facilitador: str
    tipo_servicio: str
    hora_entrada: datetime
    hora_salida: Optional[datetime] = None
    duracion_horas: Optional[float] = None
    fecha: date
    observaciones: Optional[str] = None
    sucursal_id: Optional[int] = None

    class Config:
        orm_mode = True


class ResumenHorasFacilitador(BaseModel):
    usuario_id: int
    nombre_completo: str
    tipo_servicio: str
    total_registros: int
    total_horas: float
