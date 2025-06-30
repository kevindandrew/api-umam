from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import Horario, DiasClase, Hora, DiaSemana, Curso, Aula, Usuario, Gestion, Matricula
from app.schemas.horario import *
from app.database import get_session
from app.dependencies import get_current_active_user
from typing import List
from app.dependencies import require_admin_or_encargado
router = APIRouter(prefix="/horarios", tags=["Horarios"])

# Crear horario completo


@router.post("/", response_model=HorarioOut)
def crear_horario(horario_in: HorarioCreate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    nuevo_horario = Horario(
        curso_id=horario_in.curso_id,
        aula_id=horario_in.aula_id,
        profesor_id=horario_in.profesor_id,
        gestion_id=horario_in.gestion_id,
        activo=horario_in.activo
    )
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)

    for dia in horario_in.dias_clase:
        dia_clase = DiasClase(
            horario_id=nuevo_horario.horario_id,
            dia_semana_id=dia.dia_semana_id,
            hora_id=dia.hora_id
        )
        db.add(dia_clase)

    db.commit()
    db.refresh(nuevo_horario)
    return nuevo_horario

# Obtener todos los horarios (con filtro opcional por gestion_id)


@router.get("/", response_model=List[HorarioOut])
def obtener_horarios(
    gestion_id: Optional[int] = Query(None),
    sucursal_id: Optional[int] = Query(None),
    aula_id: Optional[int] = Query(None),
    usuario_id: Optional[int] = Query(None),
    curso_id: Optional[int] = Query(None),
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_active_user)
):
    query = db.query(Horario)

    if gestion_id is not None:
        query = query.filter(Horario.gestion_id == gestion_id)
    if sucursal_id is not None:
        query = query.join(Horario.aula).filter(
            Aula.sucursal_id == sucursal_id)
    if aula_id is not None:
        query = query.filter(Horario.aula_id == aula_id)
    if usuario_id is not None:
        query = query.filter(Horario.profesor_id == usuario_id)
    if curso_id is not None:
        query = query.filter(Horario.curso_id == curso_id)

    return query.all()


# Actualizar un horario


@router.put("/{horario_id}", response_model=HorarioOut)
def actualizar_horario(horario_id: int, datos: HorarioUpdate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    horario = db.query(Horario).filter(
        Horario.horario_id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(horario, campo, valor)

    db.commit()
    db.refresh(horario)
    return horario

# Eliminar un horario


@router.delete("/{horario_id}", status_code=204)
def eliminar_horario(horario_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    # Verificar si el horario existe
    horario = db.query(Horario).filter(
        Horario.horario_id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    try:
        # 1. Eliminar o actualizar matrículas relacionadas
        # Opción A: Eliminar matrículas (si es aceptable en tu modelo de negocio)
        db.query(Matricula).filter(Matricula.horario_id == horario_id).delete()

        # Opción B: O establecer horario_id a NULL si la columna lo permite
        # (necesitarías cambiar el esquema de la tabla para permitir NULL)
        # db.query(Matricula).filter(Matricula.horario_id == horario_id).update({"horario_id": None})

        # 2. Eliminar días de clase asociados
        db.query(DiasClase).filter(DiasClase.horario_id == horario_id).delete()

        # 3. Finalmente eliminar el horario
        db.delete(horario)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"No se pudo eliminar el horario: {str(e)}")

    return

# Listar horas disponibles


@router.get("/horas", response_model=List[HoraOut])
def listar_horas(db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_active_user)):
    return db.query(Hora).all()

# ✅ POST nueva hora


@router.post("/horas", response_model=HoraOut)
def crear_hora(hora: HoraCreate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    nueva_hora = Hora(**hora.dict())
    db.add(nueva_hora)
    db.commit()
    db.refresh(nueva_hora)
    return nueva_hora

# ✅ PUT actualizar una hora


@router.put("/horas/{hora_id}", response_model=HoraOut)
def actualizar_hora(hora_id: int, datos: HoraUpdate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    hora = db.query(Hora).filter(Hora.hora_id == hora_id).first()
    if not hora:
        raise HTTPException(status_code=404, detail="Hora no encontrada")

    for key, value in datos.dict().items():
        setattr(hora, key, value)

    db.commit()
    db.refresh(hora)
    return hora

# ✅ DELETE eliminar una hora


@router.delete("/horas/{hora_id}")
def eliminar_hora(hora_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    hora = db.query(Hora).filter(Hora.hora_id == hora_id).first()
    if not hora:
        raise HTTPException(status_code=404, detail="Hora no encontrada")

    db.delete(hora)
    db.commit()
    return {"mensaje": "Hora eliminada correctamente"}

# Listar días de la semana


@router.get("/dias-semana", response_model=List[DiaSemanaOut])
def listar_dias_semana(db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_active_user)):
    return db.query(DiaSemana).all()


# Obtener un horario específico


@router.get("/{horario_id}", response_model=HorarioOut)
def obtener_horario(horario_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_active_user)):
    horario = db.query(Horario).filter(
        Horario.horario_id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario
