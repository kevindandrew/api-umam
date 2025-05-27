from sqlmodel import SQLModel


class RolBase(SQLModel):
    """Schema base para Rol"""
    nombre: str


class RolCreate(RolBase):
    """Schema para creación de roles (POST)"""
    pass


class RolRead(RolBase):
    """Schema para lectura de roles (GET)"""
    rol_id: int
