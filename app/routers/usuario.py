from app.security import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.sucursal import Sucursal
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.database import get_session
from app.dependencies import require_admin
router = APIRouter(prefix="/usuarios", tags=["Usuarios"],)


# GET con filtros opcionales
@router.get("/", response_model=List[UsuarioOut])
def get_usuarios(
    sucursal_id: Optional[int] = Query(None),
    rol_id: Optional[int] = Query(None),
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    query = db.query(Usuario)

    if sucursal_id is not None:
        query = query.filter(Usuario.sucursal_id == sucursal_id)

    if rol_id is not None:
        query = query.filter(Usuario.rol_id == rol_id)

    return query.all()


@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_usuario(usuario_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    usuario = db.query(Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioOut, status_code=201)
def create_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    hashed_password = get_password_hash(usuario_in.password)
    usuario_data = usuario_in.dict()
    usuario_data["password"] = hashed_password

    usuario = Usuario(**usuario_data)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_usuario(usuario_id: int, usuario_in: UsuarioUpdate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    usuario = db.query(Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for field, value in usuario_in.dict(exclude_unset=True).items():
        setattr(usuario, field, value)

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=204)
def delete_usuario(usuario_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    usuario = db.query(Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
