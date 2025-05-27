from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Optional
from jose import JWTError, jwt
from app.database import get_session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.security import AuthConfig

# Seguridad con esquema Bearer
security = HTTPBearer()

# 1. Decodifica el token y obtiene el payload


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, AuthConfig.SECRET_KEY,
                             algorithms=[AuthConfig.ALGORITHM])
        return payload
    except JWTError:
        return None

# 2. Obtiene el usuario actual desde el token


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> Usuario:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.exec(select(Usuario).where(Usuario.username == username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user

# 3. Versión simplificada sin verificación adicional


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    return current_user

# 4. Fábrica para verificar roles


def require_role(*allowed_roles: str):
    async def role_checker(
        current_user: Usuario = Depends(get_current_active_user),
        db: Session = Depends(get_session)
    ) -> Usuario:
        rol = db.exec(select(Rol).where(
            Rol.rol_id == current_user.rol_id)).first()

        if not rol or rol.nombre.lower() not in [r.lower() for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


# 5. Dependencias listas para usar
require_admin = require_role("administrador")
require_encargado = require_role("encargado_sucursal")
require_facilitador = require_role("facilitador")
require_admin_or_facilitador = require_role("administrador", "facilitador")
require_admin_or_encargado = require_role(
    "administrador", "encargado_sucursal")

# 6. (Opcional) Verifica acceso a una sucursal específica


def require_sucursal(sucursal_id: int = None):
    async def sucursal_checker(
        current_user: Usuario = Depends(get_current_active_user)
    ) -> Usuario:
        if current_user.rol.nombre.lower() == "administrador":
            return current_user

        if sucursal_id and current_user.sucursal_id != sucursal_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a esta sucursal"
            )
        return current_user
    return sucursal_checker
