from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.sucursal import Sucursal
from app.models.aula import Aula
from app.schemas.sucursal import (
    SucursalCreate, SucursalUpdate, SucursalOut,
    AulaCreate, AulaUpdate, AulaOut
)
from app.database import get_session
from app.dependencies import get_current_active_user, require_admin, require_encargado, require_admin_or_encargado
from app.models.usuario import Usuario

router = APIRouter(prefix="/sucursales", tags=["Sucursales"])

# ----------------------
# 📍 Sucursales
# ----------------------


@router.get("/", response_model=List[SucursalOut])
def listar_sucursales(
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_active_user)
):
    return db.query(Sucursal).all()


@router.post("/", response_model=SucursalOut)
def crear_sucursal(
    sucursal_in: SucursalCreate,
    db: Session = Depends(get_session),
    user: Usuario = Depends(require_admin_or_encargado)
):
    sucursal = Sucursal(**sucursal_in.dict())
    db.add(sucursal)
    db.commit()
    db.refresh(sucursal)
    return sucursal


@router.put("/{sucursal_id}", response_model=SucursalOut)
def actualizar_sucursal(
    sucursal_id: int,
    sucursal_in: SucursalUpdate,
    db: Session = Depends(get_session),
    user: Usuario = Depends(require_admin_or_encargado)
):
    sucursal = db.query(Sucursal).get(sucursal_id)
    if not sucursal:
        raise HTTPException(404, "Sucursal no encontrada")

    for key, value in sucursal_in.dict(exclude_unset=True).items():
        setattr(sucursal, key, value)

    db.commit()
    db.refresh(sucursal)
    return sucursal


@router.delete("/{sucursal_id}", status_code=204)
def eliminar_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_session),
    user: Usuario = Depends(require_admin_or_encargado)
):
    sucursal = db.query(Sucursal).get(sucursal_id)
    if not sucursal:
        raise HTTPException(404, "Sucursal no encontrada")

    db.delete(sucursal)
    db.commit()


# ----------------------
# 🏫 Aulas por sucursal
# ----------------------

@router.get("/{sucursal_id}/aulas", response_model=List[AulaOut])
def listar_aulas(
    sucursal_id: int,
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_active_user)
):
    return db.query(Aula).filter(Aula.sucursal_id == sucursal_id).all()


@router.post("/{sucursal_id}/aulas", response_model=AulaOut)
def crear_aula(
    sucursal_id: int,
    aula_in: AulaCreate,
    db: Session = Depends(get_session),
    user: Usuario = Depends(require_admin_or_encargado)
):
    # Asegurar que el aula pertenezca a la sucursal
    if aula_in.sucursal_id != sucursal_id:
        raise HTTPException(400, "Sucursal no coincide")

    aula = Aula(**aula_in.dict())
    db.add(aula)
    db.commit()
    db.refresh(aula)
    return aula


@router.put("/aulas/{aula_id}", response_model=AulaOut)
def actualizar_aula(
    aula_id: int,
    aula_in: AulaUpdate,
    db: Session = Depends(get_session),
    user: Usuario = Depends(require_admin_or_encargado)
):
    aula = db.query(Aula).get(aula_id)
    if not aula:
        raise HTTPException(404, "Aula no encontrada")

    for key, value in aula_in.dict(exclude_unset=True).items():
        setattr(aula, key, value)

    db.commit()
    db.refresh(aula)
    return aula


@router.delete("/aulas/{aula_id}", status_code=204)
def eliminar_aula(
    aula_id: int,
    db: Session = Depends(get_session),
    user: Usuario = Depends(require_admin_or_encargado)
):
    aula = db.query(Aula).get(aula_id)
    if not aula:
        raise HTTPException(404, "Aula no encontrada")
    db.delete(aula)
    db.commit()
