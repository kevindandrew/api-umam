from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import Horario, DiasClase, Hora, DiaSemana, Curso, Aula, Usuario, Gestion, Matricula, CursoSucursal
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

# Transferir un horario completo (aula, sucursal, profesor, días) a otra sucursal/aula


@router.post("/{horario_id}/transferir", response_model=HorarioOut)
def transferir_horario(
    horario_id: int,
    datos: HorarioTransferIn,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin_or_encargado)
):
    # 1. Verificar que el horario existe
    horario = db.query(Horario).filter(Horario.horario_id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    # 2. Verificar que el aula destino existe
    nueva_aula = db.query(Aula).filter(Aula.aula_id == datos.aula_id).first()
    if not nueva_aula:
        raise HTTPException(status_code=404, detail="Aula destino no encontrada")

    # 3. Verificar capacidad del aula destino vs alumnos activos inscritos
    total_inscritos = db.query(Matricula).filter(
        Matricula.horario_id == horario_id,
        Matricula.estado == "activo"
    ).count()

    if total_inscritos > nueva_aula.capacidad:
        raise HTTPException(
            status_code=400,
            detail=(
                f"El aula destino no tiene capacidad suficiente. "
                f"Capacidad del aula: {nueva_aula.capacidad}, "
                f"Estudiantes inscritos activos: {total_inscritos}"
            )
        )

    # 4. Determinar los días/horas que se usarán (nuevos o los actuales)
    dias_a_usar = datos.dias_clase if datos.dias_clase is not None else [
        DiaClaseBase(dia_semana_id=d.dia_semana_id, hora_id=d.hora_id)
        for d in horario.dias_clase
    ]

    # 5. Verificar conflictos de horario en el aula destino
    horarios_en_aula_destino = db.query(Horario).filter(
        Horario.aula_id == datos.aula_id,
        Horario.horario_id != horario_id,
        Horario.activo == True
    ).all()

    ocupados = set()
    for h in horarios_en_aula_destino:
        for d in h.dias_clase:
            ocupados.add((d.dia_semana_id, d.hora_id))

    for dia in dias_a_usar:
        if (dia.dia_semana_id, dia.hora_id) in ocupados:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Conflicto de horario en el aula destino: "
                    f"dia_semana_id={dia.dia_semana_id}, hora_id={dia.hora_id} ya está ocupado"
                )
            )

    # 6. Verificar que el nuevo profesor existe (si se proporcionó)
    if datos.profesor_id is not None:
        profesor = db.query(Usuario).filter(Usuario.usuario_id == datos.profesor_id).first()
        if not profesor:
            raise HTTPException(status_code=404, detail="Profesor no encontrado")
        horario.profesor_id = datos.profesor_id

    # 7. Asegurar que el curso esté asignado a la sucursal destino
    sucursal_destino_id = nueva_aula.sucursal_id
    curso_sucursal_existente = db.query(CursoSucursal).filter(
        CursoSucursal.curso_id == horario.curso_id,
        CursoSucursal.sucursal_id == sucursal_destino_id,
        CursoSucursal.gestion_id == horario.gestion_id
    ).first()

    if not curso_sucursal_existente:
        nueva_asignacion = CursoSucursal(
            curso_id=horario.curso_id,
            sucursal_id=sucursal_destino_id,
            gestion_id=horario.gestion_id
        )
        db.add(nueva_asignacion)

    # 8. Actualizar el aula del horario
    horario.aula_id = datos.aula_id

    # 9. Actualizar días/horas si se proporcionaron nuevos
    if datos.dias_clase is not None:
        db.query(DiasClase).filter(DiasClase.horario_id == horario_id).delete()
        for dia in datos.dias_clase:
            nuevo_dia = DiasClase(
                horario_id=horario_id,
                dia_semana_id=dia.dia_semana_id,
                hora_id=dia.hora_id
            )
            db.add(nuevo_dia)

    db.commit()
    db.refresh(horario)
    return horario


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
