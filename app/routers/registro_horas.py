from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_session
from app.models.registro_horas import RegistroHoras
from app.models.usuario import Usuario
from app.dependencies import (
    require_facilitador,
    require_admin_or_encargado,
    get_current_active_user,
)
from app.schemas.registro_horas import (
    RegistroHorasCreate,
    RegistroHorasOut,
    ResumenHorasFacilitador,
)

router = APIRouter(prefix="/registro-horas", tags=["Registro de Horas"])


def _to_out(registro: RegistroHoras, usuario: Usuario) -> RegistroHorasOut:
    return RegistroHorasOut(
        registro_id=registro.registro_id,
        usuario_id=registro.usuario_id,
        nombre_facilitador=f"{usuario.nombres} {usuario.ap_paterno} {usuario.ap_materno}",
        tipo_servicio=registro.tipo_servicio,
        hora_entrada=registro.hora_entrada,
        hora_salida=registro.hora_salida,
        duracion_horas=float(registro.duracion_horas) if registro.duracion_horas is not None else None,
        fecha=registro.fecha,
        observaciones=registro.observaciones,
        sucursal_id=registro.sucursal_id,
    )


@router.post("/entrada", response_model=RegistroHorasOut)
def fichar_entrada(
    data: RegistroHorasCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_facilitador),
):
    sesion_abierta = (
        db.query(RegistroHoras)
        .filter(
            RegistroHoras.usuario_id == current_user.usuario_id,
            RegistroHoras.hora_salida == None,
        )
        .first()
    )
    if sesion_abierta:
        raise HTTPException(
            status_code=400,
            detail=f"Ya tienes una sesión abierta (ID: {sesion_abierta.registro_id}). Registra tu salida primero.",
        )

    ahora = datetime.utcnow()
    registro = RegistroHoras(
        usuario_id=current_user.usuario_id,
        tipo_servicio=data.tipo_servicio.value,
        hora_entrada=ahora,
        fecha=ahora.date(),
        observaciones=data.observaciones,
        sucursal_id=data.sucursal_id if data.sucursal_id is not None else current_user.sucursal_id,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return _to_out(registro, current_user)


@router.put("/{registro_id}/salida", response_model=RegistroHorasOut)
def fichar_salida(
    registro_id: int,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_facilitador),
):
    registro = (
        db.query(RegistroHoras)
        .filter(
            RegistroHoras.registro_id == registro_id,
            RegistroHoras.usuario_id == current_user.usuario_id,
        )
        .first()
    )
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    if registro.hora_salida is not None:
        raise HTTPException(status_code=400, detail="Este registro ya tiene hora de salida registrada")

    ahora = datetime.utcnow()
    registro.hora_salida = ahora
    delta = ahora - registro.hora_entrada
    registro.duracion_horas = round(delta.total_seconds() / 3600, 2)

    db.commit()
    db.refresh(registro)
    return _to_out(registro, current_user)


@router.get("/mis-registros", response_model=list[RegistroHorasOut])
def mis_registros(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    tipo_servicio: Optional[str] = Query(None),
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_facilitador),
):
    query = db.query(RegistroHoras).filter(
        RegistroHoras.usuario_id == current_user.usuario_id
    )
    if fecha_inicio:
        query = query.filter(RegistroHoras.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(RegistroHoras.fecha <= fecha_fin)
    if tipo_servicio:
        query = query.filter(RegistroHoras.tipo_servicio == tipo_servicio)

    registros = query.order_by(RegistroHoras.hora_entrada.desc()).all()
    return [_to_out(r, current_user) for r in registros]


@router.get("/", response_model=list[RegistroHorasOut])
def listar_todos(
    usuario_id: Optional[int] = Query(None),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    tipo_servicio: Optional[str] = Query(None),
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin_or_encargado),
):
    query = db.query(RegistroHoras, Usuario).join(
        Usuario, Usuario.usuario_id == RegistroHoras.usuario_id
    )
    if usuario_id:
        query = query.filter(RegistroHoras.usuario_id == usuario_id)
    if fecha_inicio:
        query = query.filter(RegistroHoras.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(RegistroHoras.fecha <= fecha_fin)
    if tipo_servicio:
        query = query.filter(RegistroHoras.tipo_servicio == tipo_servicio)

    resultados = query.order_by(RegistroHoras.hora_entrada.desc()).all()
    return [_to_out(r, u) for r, u in resultados]


@router.get("/resumen/{usuario_id}", response_model=list[ResumenHorasFacilitador])
def resumen_facilitador(
    usuario_id: int,
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin_or_encargado),
):
    facilitador = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not facilitador:
        raise HTTPException(status_code=404, detail="Facilitador no encontrado")

    query = db.query(
        RegistroHoras.tipo_servicio,
        func.count(RegistroHoras.registro_id).label("total_registros"),
        func.coalesce(func.sum(RegistroHoras.duracion_horas), 0).label("total_horas"),
    ).filter(
        RegistroHoras.usuario_id == usuario_id,
        RegistroHoras.hora_salida.isnot(None),
    )
    if fecha_inicio:
        query = query.filter(RegistroHoras.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(RegistroHoras.fecha <= fecha_fin)

    resultados = query.group_by(RegistroHoras.tipo_servicio).all()
    nombre_completo = f"{facilitador.nombres} {facilitador.ap_paterno} {facilitador.ap_materno}"

    return [
        ResumenHorasFacilitador(
            usuario_id=usuario_id,
            nombre_completo=nombre_completo,
            tipo_servicio=r.tipo_servicio,
            total_registros=r.total_registros,
            total_horas=float(r.total_horas),
        )
        for r in resultados
    ]
