from pydantic import BaseModel
from typing import Optional, List


# -------------------------------------
# 📚 Curso Schemas
# -------------------------------------

class CursoBase(BaseModel):
    nombre: str
    gestoria: bool


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    nombre: Optional[str] = None
    gestoria: Optional[bool] = None


class CursoOut(CursoBase):
    curso_id: int

    class Config:
        orm_mode = True


# -------------------------------------
# 👨‍🏫 CursoDocente Schemas
# -------------------------------------

class CursoDocenteBase(BaseModel):
    curso_id: int
    usuario_id: int
    gestion_id: int


class CursoDocenteCreate(CursoDocenteBase):
    pass


class CursoDocenteOut(CursoDocenteBase):
    curso_docente_id: int

    class Config:
        orm_mode = True


# -------------------------------------
# 🏢 CursoSucursal Schemas
# -------------------------------------

class CursoSucursalBase(BaseModel):
    curso_id: int
    sucursal_id: int
    gestion_id: int


class CursoSucursalCreate(CursoSucursalBase):
    pass


class CursoSucursalOut(CursoSucursalBase):
    curso_sucursal_id: int

    class Config:
        orm_mode = True


# -------------------------------------
# 📅 Gestión Schemas
# -------------------------------------

class GestionBase(BaseModel):
    gestion: str
    year_id: int


class GestionCreate(GestionBase):
    pass


class GestionOut(GestionBase):
    gestion_id: int

    class Config:
        orm_mode = True


class GestionUpdate(BaseModel):
    gestion: Optional[str] = None
    year_id: Optional[int] = None
# -------------------------------------
# 📅 Year Schemas
# -------------------------------------


class YearBase(BaseModel):
    year: str


class YearCreate(YearBase):
    pass


class YearUpdate(BaseModel):
    year: Optional[str] = None


class YearOut(YearBase):
    year_id: int

    class Config:
        orm_mode = True
