from pydantic import BaseModel
from typing import List, Optional
from datetime import time


# ----- HORA -----
class HoraBase(BaseModel):
    hora_inicio: time
    hora_fin: time


class HoraCreate(HoraBase):
    pass


class HoraUpdate(HoraBase):
    pass


class HoraOut(HoraBase):
    hora_id: int

    class Config:
        orm_mode = True


# ----- DÍA SEMANA -----
class DiaSemanaBase(BaseModel):
    dia_semana: str


class DiaSemanaCreate(DiaSemanaBase):
    pass


class DiaSemanaOut(DiaSemanaBase):
    dias_semana_id: int

    class Config:
        orm_mode = True


# ----- AULA -----
class AulaBase(BaseModel):
    nombre_aula: str
    capacidad: int
    sucursal_id: int


class AulaCreate(AulaBase):
    pass


class AulaOut(AulaBase):
    aula_id: int

    class Config:
        orm_mode = True


# ----- DÍAS CLASE -----
class DiaClaseBase(BaseModel):
    dia_semana_id: int
    hora_id: int
    aula_id: Optional[int] = None


class DiaClaseCreate(DiaClaseBase):
    pass


class DiaClaseOut(DiaClaseBase):
    dia_clase_id: int
    dia_semana: DiaSemanaOut
    hora: HoraOut
    aula: Optional[AulaOut] = None

    class Config:
        orm_mode = True


# ----- HORARIO -----
class HorarioBase(BaseModel):
    curso_id: int
    aula_id: int
    profesor_id: int
    gestion_id: int
    activo: Optional[bool] = True


class HorarioCreate(HorarioBase):
    dias_clase: List[DiaClaseBase]


class HorarioUpdate(BaseModel):
    curso_id: Optional[int] = None
    aula_id: Optional[int] = None
    profesor_id: Optional[int] = None
    gestion_id: Optional[int] = None
    activo: Optional[bool] = None
    dias_clase: Optional[List[DiaClaseBase]] = None


class HorarioOut(HorarioBase):
    horario_id: int
    dias_clase: List[DiaClaseOut]

    class Config:
        orm_mode = True


# ----- TRANSFERENCIA DE HORARIO -----
class HorarioTransferIn(BaseModel):
    aula_id: int
    profesor_id: Optional[int] = None
    dias_clase: Optional[List[DiaClaseBase]] = None


# ----- DUPLICADOS Y FUSIÓN -----
class FusionarHorarioIn(BaseModel):
    target_horario_id: int


class HorarioEnGrupoOut(BaseModel):
    horario_id: int
    inscritos: int
    dias_clase: List[DiaClaseOut]

    class Config:
        orm_mode = True


class GrupoDuplicadoOut(BaseModel):
    curso_id: int
    profesor_id: int
    gestion_id: int
    aula_id: int
    horarios: List[HorarioEnGrupoOut]


class HorarioFusionadoOut(HorarioOut):
    inscritos: int
