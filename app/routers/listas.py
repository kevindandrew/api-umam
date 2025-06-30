# app/routers/listas.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.aula import Aula
from app.models.estudiante import Estudiante
from app.models.matricula import Matricula
from app.models.horario import Horario
from app.models.curso import Curso
from app.models.gestion import Gestion
# Asegúrate que el modelo exista y esté bien definido
from app.models.usuario import Usuario
from app.models.sucursal import Sucursal  # Asegúrate que exista
from app.schemas.listas import EstudianteOut, HorarioConEstudiantesOut, ActualizarNota, EstudianteConNotaOut
from sqlmodel import select
from sqlalchemy.orm import joinedload
from app.dependencies import get_current_active_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/listas", tags=["Listas"])

# 🔍 Endpoint general con filtros opcionales


@router.get("/estudiantes", response_model=List[EstudianteConNotaOut])
def listar_estudiantes_inscritos(
    sucursal_id: int = Query(None),
    gestion_id: int = Query(None),
    curso_id: int = Query(None),
    profesor_id: int = Query(None),
    db: Session = Depends(get_session),
    usuario: Usuario = Depends(get_current_active_user)
):
    query = db.query(Matricula).join(
        Estudiante, Estudiante.estudiante_id == Matricula.estudiante_id
    ).join(
        Horario, Matricula.horario_id == Horario.horario_id
    ).join(
        Curso, Horario.curso_id == Curso.curso_id
    ).join(
        Gestion, Matricula.gestion_id == Gestion.gestion_id
    )

    if sucursal_id:
        query = query.join(Aula, Aula.aula_id == Horario.aula_id).filter(
            Aula.sucursal_id == sucursal_id)

    if gestion_id:
        query = query.filter(Gestion.gestion_id == gestion_id)

    if curso_id:
        query = query.filter(Curso.curso_id == curso_id)

    if profesor_id:
        query = query.filter(Horario.profesor_id == profesor_id)

    matriculas = query.distinct().all()

    estudiantes = []
    for m in matriculas:
        estudiante = m.estudiante
        estudiantes.append({
            "matricula_id": m.matricula_id,  # ✅ Agregado
            "estudiante_id": estudiante.estudiante_id,
            "nombres": estudiante.nombres,
            "ap_paterno": estudiante.ap_paterno,
            "ap_materno": estudiante.ap_materno,
            "ci": estudiante.ci,
            "telefono": estudiante.telefono,
            "nota_final": m.nota_final,
            "estado": m.estado
        })

    return estudiantes

# 👨‍🏫 Endpoint para ver horarios de un profesor con estudiantes por clase


@router.get("/profesor/{profesor_id}/horarios", response_model=List[HorarioConEstudiantesOut])
def horarios_con_estudiantes_por_profesor(profesor_id: int, db: Session = Depends(get_session), usuario: Usuario = Depends(get_current_active_user)):
    horarios = db.query(Horario).options(
        joinedload(Horario.matriculas).joinedload(Matricula.estudiante)
    ).filter(
        Horario.profesor_id == profesor_id
    ).all()

    resultados = []
    for horario in horarios:
        estudiantes = []
        for matricula in horario.matriculas:
            estudiante = matricula.estudiante
            estudiantes.append({
                "matricula_id": matricula.matricula_id,
                "estudiante_id": estudiante.estudiante_id,
                "nombres": estudiante.nombres,
                "ap_paterno": estudiante.ap_paterno,
                "ap_materno": estudiante.ap_materno,
                "ci": estudiante.ci,
                "telefono": estudiante.telefono,
                "nota_final": matricula.nota_final,  # ⬅️ añadimos nota
                "estado": matricula.estado           # ⬅️ y estado
            })

        resultados.append({
            "horario_id": horario.horario_id,
            "curso_id": horario.curso_id,
            "aula_id": horario.aula_id,
            "profesor_id": horario.profesor_id,
            "gestion_id": horario.gestion_id,
            "activo": horario.activo,
            "estudiantes": estudiantes
        })

    return resultados


@router.put("/matricula/{matricula_id}/nota", status_code=200)
def actualizar_nota_estudiante(
    matricula_id: int,
    datos: ActualizarNota,
    db: Session = Depends(get_session),
    usuario: Usuario = Depends(get_current_active_user)
):
    matricula = db.query(Matricula).filter(
        Matricula.matricula_id == matricula_id).first()

    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula no encontrada"
        )

    matricula.nota_final = datos.nota_final
    matricula.estado = "Aprobado" if datos.nota_final >= 51 else "Reprobado"
    db.commit()

    return {"mensaje": "Nota actualizada correctamente", "estado": matricula.estado}
