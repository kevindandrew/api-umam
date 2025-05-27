import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Any, Dict, Optional, Tuple
from app.database import get_session
from app.models.usuario import Usuario

# ----------------------------
# 1. CONFIGURACIÓN SEGURA
# ----------------------------
load_dotenv()


class AuthConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY or len(SECRET_KEY) < 32:
        raise ValueError("SECRET_KEY debe tener al menos 32 caracteres")

    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


# ----------------------------
# 2. CONTEXTO DE SEGURIDAD
# ----------------------------
pwd_context = CryptContext(
    schemes=["bcrypt", "argon2"],
    deprecated="auto",
    bcrypt__rounds=12,
    argon2__time_cost=3,
    argon2__memory_cost=65536,
    argon2__parallelism=4
)

security = HTTPBearer(
    bearerFormat="JWT",
    description="Ingrese el token JWT en el formato: Bearer <token>"
)

# ----------------------------
# 3. FUNCIONES MEJORADAS
# ----------------------------


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)


def create_tokens(username: str) -> Tuple[str, str]:
    access_expire = timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expire = timedelta(days=AuthConfig.REFRESH_TOKEN_EXPIRE_DAYS)

    access_payload = {
        "sub": username,
        "type": "access",
        "exp": datetime.utcnow() + access_expire
    }

    refresh_payload = {
        "sub": username,
        "type": "refresh",
        "exp": datetime.utcnow() + refresh_expire
    }

    access_token = jwt.encode(
        access_payload, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)
    refresh_token = jwt.encode(
        refresh_payload, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)

    return access_token, refresh_token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ----------------------------
# 4. VALIDACIÓN DE TOKENS (SIN ACTIVO)
# ----------------------------


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> Usuario:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, AuthConfig.SECRET_KEY,
                             algorithms=[AuthConfig.ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido"
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        user = db.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )

        request.state.user = user
        return user

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error de token: {str(e)}"
        )

# ----------------------------
# 5. FUNCIONES ADICIONALES
# ----------------------------


def validate_refresh_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, AuthConfig.SECRET_KEY,
                             algorithms=[AuthConfig.ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload.get("sub")
    except JWTError:
        return None
