from pydantic import BaseModel, Field
from typing import Optional

# Roles predefinidos


class RolPredefinido:
    ADMINISTRADOR = "administrador"
    ENCARGADO = "encargado_sucursal"
    FACILITADOR = "facilitador"

# Request Schemas


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="admin")
    password: str = Field(..., min_length=4,
                          max_length=100, example="password123")


class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Response Schemas


class RolResponse(BaseModel):
    rol_id: int
    nombre: str = Field(..., enum=[
        RolPredefinido.ADMINISTRADOR,
        RolPredefinido.ENCARGADO,
        RolPredefinido.FACILITADOR
    ])


class UsuarioAuthResponse(BaseModel):
    usuario_id: int
    username: str
    nombres: str
    ap_paterno: str
    rol: RolResponse


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginResponse(BaseModel):
    user: UsuarioAuthResponse
    tokens: TokenResponse
