# 📦 app/routers/reportes.py
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.database import get_session
from app.models import Matricula, Horario, Aula, Sucursal, Gestion, Curso, Usuario
from app.schemas.reportes import ReporteSucursalOut, ReporteGestionOut, ReporteCursoOut, ReporteFacilitadorOut, ReporteGeneralOut
from sqlalchemy import case
from sqlalchemy import case, and_  # <- asegúrate que 'and_' esté importado


router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/general", response_model=ReporteGeneralOut)
def reporte_general(
    sucursal_id: Optional[int] = Query(None),
    gestion_id: Optional[int] = Query(None),
    curso_id: Optional[int] = Query(None),
    profesor_id: Optional[int] = Query(None),
    db: Session = Depends(get_session)
):
    query = db.query(Matricula)

    # Joins necesarios
    query = query.join(Matricula.horario).join(Horario.aula).join(
        Horario.curso).join(Horario.profesor).join(Horario.gestion)

    filtros = []
    if sucursal_id:
        filtros.append(Aula.sucursal_id == sucursal_id)
    if gestion_id:
        filtros.append(Horario.gestion_id == gestion_id)
    if curso_id:
        filtros.append(Horario.curso_id == curso_id)
    if profesor_id:
        filtros.append(Horario.profesor_id == profesor_id)

    if filtros:
        query = query.filter(and_(*filtros))

    total = query.distinct(Matricula.estudiante_id,
                           Matricula.horario_id).count()

    aprobados = query.filter(Matricula.estado == "Aprobado").count()
    reprobados = query.filter(Matricula.estado == "Reprobado").count()

    return ReporteGeneralOut(
        total_estudiantes=total,
        aprobados=aprobados,
        reprobados=reprobados,
        porcentaje_aprobados=round(
            (aprobados / total) * 100, 2) if total else 0.0,
        porcentaje_reprobados=round(
            (reprobados / total) * 100, 2) if total else 0.0
    )

# 📊 1. Reporte por Sucursal


@router.get("/por-sucursal", response_model=list[ReporteSucursalOut])
def reporte_por_sucursal(db: Session = Depends(get_session)):
    subquery = (
        db.query(
            Sucursal.sucursal_id,
            Sucursal.nombre,
            Matricula.estudiante_id,
            Matricula.estado
        )
        .join(Aula, Aula.sucursal_id == Sucursal.sucursal_id)
        .join(Horario, Horario.aula_id == Aula.aula_id)
        .join(Matricula, Matricula.horario_id == Horario.horario_id)
        .distinct(Sucursal.sucursal_id, Matricula.estudiante_id)
        .subquery()
    )

    resultados = (
        db.query(
            subquery.c.sucursal_id,
            subquery.c.nombre,
            func.count().label("total"),
            func.sum(case((subquery.c.estado == "Aprobado", 1), else_=0)).label(
                "aprobados"),
            func.sum(case((subquery.c.estado == "Reprobado", 1), else_=0)).label(
                "reprobados"),

        )
        .group_by(subquery.c.sucursal_id, subquery.c.nombre)
        .all()
    )

    return [
        ReporteSucursalOut(
            sucursal_id=r.sucursal_id,
            nombre=r.nombre,
            total_estudiantes=r.total,
            aprobados=r.aprobados,
            reprobados=r.reprobados,
            porcentaje_aprobados=round(
                (r.aprobados / r.total) * 100, 2) if r.total else 0.0,
            porcentaje_reprobados=round(
                (r.reprobados / r.total) * 100, 2) if r.total else 0.0
        ) for r in resultados
    ]

# 📊 2. Reporte por Gestión


@router.get("/por-gestion", response_model=list[ReporteGestionOut])
def reporte_por_gestion(db: Session = Depends(get_session)):
    resultados = (
        db.query(
            Gestion.gestion_id,
            Gestion.gestion,
            func.count(distinct(Matricula.estudiante_id)).label("total"),
            func.sum(case((Matricula.estado == "Aprobado", 1), else_=0)).label(
                "aprobados"),
            func.sum(case((Matricula.estado == "Reprobado", 1), else_=0)).label(
                "reprobados"),

        )
        .join(Matricula.gestion)
        .group_by(Gestion.gestion_id, Gestion.gestion)
        .all()
    )

    return [
        ReporteGestionOut(
            gestion_id=r.gestion_id,
            nombre=r.gestion,
            total_estudiantes=r.total,
            aprobados=r.aprobados,
            reprobados=r.reprobados,
            porcentaje_aprobados=round(
                (r.aprobados / r.total) * 100, 2) if r.total else 0.0,
            porcentaje_reprobados=round(
                (r.reprobados / r.total) * 100, 2) if r.total else 0.0
        ) for r in resultados
    ]

# 📊 3. Reporte por Curso


@router.get("/por-curso", response_model=list[ReporteCursoOut])
def reporte_por_curso(db: Session = Depends(get_session)):
    resultados = (
        db.query(
            Curso.curso_id,
            Curso.nombre,
            func.count(Matricula.estudiante_id).label("total"),
            func.sum(case((Matricula.estado == "Aprobado", 1), else_=0)).label(
                "aprobados"),
            func.sum(case((Matricula.estado == "Reprobado", 1), else_=0)).label(
                "reprobados"),

        )
        .join(Horario, Horario.curso_id == Curso.curso_id)
        .join(Matricula, Matricula.horario_id == Horario.horario_id)
        .group_by(Curso.curso_id, Curso.nombre)
        .all()
    )

    return [
        ReporteCursoOut(
            curso_id=r.curso_id,
            nombre=r.nombre,
            total_estudiantes=r.total,
            aprobados=r.aprobados,
            reprobados=r.reprobados,
            porcentaje_aprobados=round(
                (r.aprobados / r.total) * 100, 2) if r.total else 0.0,
            porcentaje_reprobados=round(
                (r.reprobados / r.total) * 100, 2) if r.total else 0.0
        ) for r in resultados
    ]

# 📊 4. Reporte por Facilitador (profesor)


@router.get("/por-facilitador", response_model=list[ReporteFacilitadorOut])
def reporte_por_facilitador(db: Session = Depends(get_session)):
    resultados = (
        db.query(
            Usuario.usuario_id,
            func.concat(Usuario.nombres, ' ', Usuario.ap_paterno,
                        ' ', Usuario.ap_materno).label("nombre_completo"),
            Gestion.gestion_id,
            func.count(Matricula.estudiante_id).label("total"),
            func.sum(case((Matricula.estado == "Aprobado", 1), else_=0)).label(
                "aprobados"),
            func.sum(case((Matricula.estado == "Reprobado", 1), else_=0)).label(
                "reprobados"),

        )
        .join(Horario, Horario.profesor_id == Usuario.usuario_id)
        .join(Gestion, Gestion.gestion_id == Horario.gestion_id)
        .join(Matricula, Matricula.horario_id == Horario.horario_id)
        .group_by(Usuario.usuario_id, "nombre_completo", Gestion.gestion_id)
        .all()
    )

    return [
        ReporteFacilitadorOut(
            profesor_id=r.usuario_id,
            nombre_completo=r.nombre_completo,
            gestion_id=r.gestion_id,
            total_estudiantes=r.total,
            aprobados=r.aprobados,
            reprobados=r.reprobados,
            porcentaje_aprobados=round(
                (r.aprobados / r.total) * 100, 2) if r.total else 0.0,
            porcentaje_reprobados=round(
                (r.reprobados / r.total) * 100, 2) if r.total else 0.0
        ) for r in resultados
    ]
