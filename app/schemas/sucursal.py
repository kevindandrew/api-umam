from pydantic import BaseModel
from typing import Optional, List


# -------------------------------
# 🏫 Aula Schemas
# -------------------------------

class AulaBase(BaseModel):
    nombre_aula: str
    capacidad: int
    sucursal_id: int


class AulaCreate(AulaBase):
    pass


class AulaUpdate(BaseModel):
    nombre_aula: Optional[str] = None
    capacidad: Optional[int] = None


class AulaOut(AulaBase):
    aula_id: int

    class Config:
        orm_mode = True


# -------------------------------
# 🏢 Sucursal Schemas
# -------------------------------

class SucursalBase(BaseModel):
    nombre: str
    direccion: str


class SucursalCreate(SucursalBase):
    pass


class SucursalUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None


class SucursalOut(SucursalBase):
    sucursal_id: int
    aulas: List[AulaOut] = []

    class Config:
        orm_mode = True
