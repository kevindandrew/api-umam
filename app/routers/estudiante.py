from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Estudiante, DatosFamiliar, DatosAcademico, DatosMedico
from app.schemas.estudiante import EstudianteCreate, EstudianteOut
from app.database import get_session
from sqlalchemy.orm import joinedload, session
from app.dependencies import require_admin_or_encargado
from app.models.usuario import Usuario

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.post("/", response_model=EstudianteOut)
def crear_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    # Crear estudiante
    nuevo_estudiante = Estudiante(
        nombres=estudiante.nombres,
        ap_paterno=estudiante.ap_paterno,
        ap_materno=estudiante.ap_materno,
        ci=estudiante.ci,
        telefono=estudiante.telefono,
        fecha_nacimiento=estudiante.fecha_nacimiento,
        genero=estudiante.genero,
        lugar_nacimiento=estudiante.lugar_nacimiento,
        estado_civil=estudiante.estado_civil,
        direccion=estudiante.direccion,
        como_se_entero=estudiante.como_se_entero
    )
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)

    # Registrar datos relacionados
    for familiar in estudiante.datos_familiares:
        db.add(DatosFamiliar(
            estudiante_id=nuevo_estudiante.estudiante_id, **familiar.dict()))
    for academico in estudiante.datos_academicos:
        db.add(DatosAcademico(
            estudiante_id=nuevo_estudiante.estudiante_id, **academico.dict()))
    for medico in estudiante.datos_medicos:
        db.add(DatosMedico(
            estudiante_id=nuevo_estudiante.estudiante_id, **medico.dict()))

    db.commit()

    # Volver a cargar con relaciones
    estudiante_con_todo = db.query(Estudiante).options(
        joinedload(Estudiante.datos_familiares),
        joinedload(Estudiante.datos_academicos),
        joinedload(Estudiante.datos_medicos)
    ).filter(Estudiante.estudiante_id == nuevo_estudiante.estudiante_id).first()

    return estudiante_con_todo


@router.get("/", response_model=List[EstudianteOut])
def obtener_estudiantes(db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    return db.query(Estudiante).all()


@router.get("/{estudiante_id}", response_model=EstudianteOut)
def obtener_estudiante(estudiante_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.estudiante_id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.put("/{estudiante_id}", response_model=EstudianteOut)
def actualizar_estudiante(estudiante_id: int, estudiante_actualizado: EstudianteCreate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.estudiante_id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    for key, value in estudiante_actualizado.dict(exclude_unset=True).items():
        setattr(estudiante, key, value)

    db.commit()
    db.refresh(estudiante)
    return estudiante


@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.estudiante_id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiante)
    db.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}
