from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    TokenResponse,
    RefreshTokenRequest,
    RolPredefinido,
    UsuarioAuthResponse,
    RolResponse,

)
from app.security import (
    create_tokens,
    verify_password,
    validate_refresh_token,
    get_current_user,
    AuthConfig
)
from app.database import get_session
from app.models.usuario import Usuario
from app.models.rol import Rol

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_session)
):
    user = db.exec(
        select(Usuario)
        .where(Usuario.username == login_data.username)
    ).first()

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Verificación de rol (opcional)
    rol = db.get(Rol, user.rol_id)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no asignado"
        )

    access_token, refresh_token = create_tokens(user.username)

    return LoginResponse(
        user=UsuarioAuthResponse(
            usuario_id=user.usuario_id,
            username=user.username,
            nombres=user.nombres,
            ap_paterno=user.ap_paterno,
            rol=RolResponse(
                rol_id=rol.rol_id,
                nombre=rol.nombre
            )
        ),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    )


@router.get("/me", response_model=UsuarioAuthResponse)
async def get_current_user_profile(
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    rol = db.get(Rol, user.rol_id)
    return UsuarioAuthResponse(
        usuario_id=user.usuario_id,
        username=user.username,
        nombres=user.nombres,
        ap_paterno=user.ap_paterno,
        rol=RolResponse(
            rol_id=rol.rol_id,
            nombre=rol.nombre
        )
    )
