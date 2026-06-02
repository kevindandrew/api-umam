from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_session
from app.dependencies import (
    get_current_active_user,
    require_admin,
    require_admin_or_facilitador,
    require_facilitador,
)
from app.models.informe_mensual import InformeMensual
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.schemas.informe_mensual import InformeMensualCreate, InformeMensualOut, InformeMensualUpdate

router = APIRouter(prefix="/informes", tags=["Control de Informes"])


def _to_out(informe: InformeMensual, usuario: Usuario) -> InformeMensualOut:
    return InformeMensualOut(
        informe_id=informe.informe_id,
        usuario_id=informe.usuario_id,
        nombre_facilitador=f"{usuario.nombres} {usuario.ap_paterno} {usuario.ap_materno}",
        carrera=informe.carrera,
        universidad=informe.universidad,
        mes=informe.mes,
        anio=informe.anio,
        actividades_realizadas=informe.actividades_realizadas,
        como_se_realizaron=informe.como_se_realizaron,
        resultados_obtenidos=informe.resultados_obtenidos,
        relacion_alcaldia=informe.relacion_alcaldia,
        medios_otorgados_alcaldia=informe.medios_otorgados_alcaldia,
        fecha_creacion=informe.fecha_creacion,
        fecha_actualizacion=informe.fecha_actualizacion,
    )


def _es_admin(db: Session, current_user: Usuario) -> bool:
    rol = db.query(Rol).filter(Rol.rol_id == current_user.rol_id).first()
    return rol is not None and rol.nombre.lower() == "administrador"


def _check_duplicado(db: Session, usuario_id: int, mes: int, anio: int, excluir_id: int = None) -> bool:
    query = db.query(InformeMensual).filter(
        InformeMensual.usuario_id == usuario_id,
        InformeMensual.mes == mes,
        InformeMensual.anio == anio,
    )
    if excluir_id:
        query = query.filter(InformeMensual.informe_id != excluir_id)
    return query.first() is not None


# --- Facilitador: crear su propio informe ---
@router.post("/", response_model=InformeMensualOut)
def crear_informe(
    data: InformeMensualCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_facilitador),
):
    if _check_duplicado(db, current_user.usuario_id, data.mes, data.anio):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un informe para {data.mes}/{data.anio}",
        )
    informe = InformeMensual(usuario_id=current_user.usuario_id, **data.dict())
    db.add(informe)
    db.commit()
    db.refresh(informe)
    return _to_out(informe, current_user)


# --- Admin: crear informe para un facilitador específico ---
@router.post("/admin/{facilitador_id}", response_model=InformeMensualOut)
def crear_informe_admin(
    facilitador_id: int,
    data: InformeMensualCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin),
):
    facilitador = db.query(Usuario).filter(Usuario.usuario_id == facilitador_id).first()
    if not facilitador:
        raise HTTPException(status_code=404, detail="Facilitador no encontrado")
    if _check_duplicado(db, facilitador_id, data.mes, data.anio):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un informe para {data.mes}/{data.anio}",
        )
    informe = InformeMensual(usuario_id=facilitador_id, **data.dict())
    db.add(informe)
    db.commit()
    db.refresh(informe)
    return _to_out(informe, facilitador)


# --- Facilitador: ver sus propios informes ---
@router.get("/mis-informes", response_model=list[InformeMensualOut])
def mis_informes(
    mes: Optional[int] = Query(None, ge=1, le=12),
    anio: Optional[int] = Query(None),
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_facilitador),
):
    query = db.query(InformeMensual).filter(InformeMensual.usuario_id == current_user.usuario_id)
    if mes is not None:
        query = query.filter(InformeMensual.mes == mes)
    if anio is not None:
        query = query.filter(InformeMensual.anio == anio)
    informes = query.order_by(InformeMensual.anio.desc(), InformeMensual.mes.desc()).all()
    return [_to_out(i, current_user) for i in informes]


# --- Admin: ver todos los informes con filtros ---
@router.get("/", response_model=list[InformeMensualOut])
def listar_informes(
    facilitador_id: Optional[int] = Query(None),
    mes: Optional[int] = Query(None, ge=1, le=12),
    anio: Optional[int] = Query(None),
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin),
):
    query = db.query(InformeMensual, Usuario).join(
        Usuario, Usuario.usuario_id == InformeMensual.usuario_id
    )
    if facilitador_id is not None:
        query = query.filter(InformeMensual.usuario_id == facilitador_id)
    if mes is not None:
        query = query.filter(InformeMensual.mes == mes)
    if anio is not None:
        query = query.filter(InformeMensual.anio == anio)
    resultados = query.order_by(InformeMensual.anio.desc(), InformeMensual.mes.desc()).all()
    return [_to_out(i, u) for i, u in resultados]


# --- Ver informe específico (facilitador ve el suyo, admin ve cualquiera) ---
@router.get("/{informe_id}", response_model=InformeMensualOut)
def obtener_informe(
    informe_id: int,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin_or_facilitador),
):
    informe = db.query(InformeMensual).filter(InformeMensual.informe_id == informe_id).first()
    if not informe:
        raise HTTPException(status_code=404, detail="Informe no encontrado")

    if not _es_admin(db, current_user) and informe.usuario_id != current_user.usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este informe")

    usuario = db.query(Usuario).filter(Usuario.usuario_id == informe.usuario_id).first()
    return _to_out(informe, usuario)


# --- Editar informe (facilitador edita el suyo, admin edita cualquiera) ---
@router.put("/{informe_id}", response_model=InformeMensualOut)
def actualizar_informe(
    informe_id: int,
    data: InformeMensualUpdate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin_or_facilitador),
):
    informe = db.query(InformeMensual).filter(InformeMensual.informe_id == informe_id).first()
    if not informe:
        raise HTTPException(status_code=404, detail="Informe no encontrado")

    if not _es_admin(db, current_user) and informe.usuario_id != current_user.usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este informe")

    campos = data.dict(exclude_unset=True)

    mes_nuevo = campos.get("mes", informe.mes)
    anio_nuevo = campos.get("anio", informe.anio)
    if (mes_nuevo != informe.mes or anio_nuevo != informe.anio):
        if _check_duplicado(db, informe.usuario_id, mes_nuevo, anio_nuevo, excluir_id=informe_id):
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un informe para {mes_nuevo}/{anio_nuevo}",
            )

    for campo, valor in campos.items():
        setattr(informe, campo, valor)

    db.commit()
    db.refresh(informe)
    usuario = db.query(Usuario).filter(Usuario.usuario_id == informe.usuario_id).first()
    return _to_out(informe, usuario)
