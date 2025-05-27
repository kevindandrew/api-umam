from pydantic import BaseModel, Field
from typing import Optional


class UsuarioBase(BaseModel):
    username: str = Field(..., max_length=50)
    nombres: str
    ap_paterno: str
    ap_materno: str
    ci: str
    telefono: Optional[str] = None
    rol_id: int
    sucursal_id: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    ap_paterno: Optional[str] = None
    ap_materno: Optional[str] = None
    telefono: Optional[str] = None
    rol_id: Optional[int] = None
    sucursal_id: Optional[int] = None
    password: Optional[str] = None


class RolOut(BaseModel):
    rol_id: int
    nombre: str

    class Config:
        orm_mode = True


class SucursalOut(BaseModel):
    sucursal_id: int
    nombre: str
    direccion: str

    class Config:
        orm_mode = True


class UsuarioOut(BaseModel):
    usuario_id: int
    username: str
    nombres: str
    ap_paterno: str
    ap_materno: str
    ci: str
    telefono: Optional[str]
    rol: RolOut
    sucursal: Optional[SucursalOut]

    class Config:
        orm_mode = True
