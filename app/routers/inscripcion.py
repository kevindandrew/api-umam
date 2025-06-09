from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models import Matricula, Estudiante, Horario, Gestion
from app.schemas.inscripcion import MatriculaCreate, MatriculaOut, MatriculaUpdate
from app.database import get_session
from app.dependencies import require_admin
from app.models.usuario import Usuario
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])

# -------------------------
# 📄 Schema de respuesta
# -------------------------


class HistorialItem(BaseModel):
    curso: str
    gestion: str
    nota_final: float | None
    estado: str
    fecha_matricula: datetime

    class Config:
        orm_mode = True

# -------------------------
# 📌 Historial académico
# -------------------------


@router.get("/historial/{estudiante_id}", response_model=List[HistorialItem])
def historial_academico(estudiante_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    estudiante = db.query(Estudiante).get(estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    matriculas = db.query(Matricula)\
        .options(
            joinedload(Matricula.horario).joinedload(Horario.curso),
            joinedload(Matricula.gestion)
    )\
        .filter(Matricula.estudiante_id == estudiante_id)\
        .all()

    historial = [
        HistorialItem(
            curso=matricula.horario.curso.nombre,
            gestion=matricula.gestion.gestion,
            nota_final=matricula.nota_final,
            estado=matricula.estado,
            fecha_matricula=matricula.fecha_matricula
        )
        for matricula in matriculas
    ]

    return historial

# 📌 Crear inscripción


@router.post("/", response_model=MatriculaOut)
def crear_inscripcion(datos: MatriculaCreate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    existe = db.query(Matricula).filter_by(
        estudiante_id=datos.estudiante_id,
        horario_id=datos.horario_id,
        gestion_id=datos.gestion_id
    ).first()

    if existe:
        raise HTTPException(status_code=400, detail="La inscripción ya existe")

    nueva = Matricula(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# 📌 Listar todas las inscripciones
@router.get("/", response_model=List[MatriculaOut])
def listar_inscripciones(db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    return db.query(Matricula).all()


# 📌 Obtener inscripción por ID
@router.get("/{matricula_id}", response_model=MatriculaOut)
def obtener_inscripcion(matricula_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    inscripcion = db.query(Matricula).get(matricula_id)
    if not inscripcion:
        raise HTTPException(
            status_code=404, detail="Inscripción no encontrada")
    return inscripcion


# 📌 Actualizar nota_final o estado
@router.put("/{matricula_id}", response_model=MatriculaOut)
def actualizar_inscripcion(matricula_id: int, datos: MatriculaUpdate, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    inscripcion = db.query(Matricula).get(matricula_id)
    if not inscripcion:
        raise HTTPException(
            status_code=404, detail="Inscripción no encontrada")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(inscripcion, campo, valor)

    db.commit()
    db.refresh(inscripcion)
    return inscripcion


# 📌 Eliminar inscripción
@router.delete("/{matricula_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_inscripcion(matricula_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin)):
    inscripcion = db.query(Matricula).get(matricula_id)
    if not inscripcion:
        raise HTTPException(
            status_code=404, detail="Inscripción no encontrada")
    db.delete(inscripcion)
    db.commit()
