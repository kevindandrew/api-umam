# 📦 app/schemas/reportes.py
from pydantic import BaseModel
from typing import List


class ReporteSucursalOut(BaseModel):
    sucursal_id: int
    nombre: str
    total_estudiantes: int
    aprobados: int
    reprobados: int
    porcentaje_aprobados: float
    porcentaje_reprobados: float


class ReporteGestionOut(BaseModel):
    gestion_id: int
    nombre: str
    total_estudiantes: int
    aprobados: int
    reprobados: int
    porcentaje_aprobados: float
    porcentaje_reprobados: float


class ReporteCursoOut(BaseModel):
    curso_id: int
    nombre: str
    total_estudiantes: int
    aprobados: int
    reprobados: int
    porcentaje_aprobados: float
    porcentaje_reprobados: float


class ReporteFacilitadorOut(BaseModel):
    profesor_id: int
    nombre_completo: str
    gestion_id: int
    total_estudiantes: int
    aprobados: int
    reprobados: int
    porcentaje_aprobados: float
    porcentaje_reprobados: float


class ReporteGeneralOut(BaseModel):
    total_estudiantes: int
    aprobados: int
    reprobados: int
    porcentaje_aprobados: float
    porcentaje_reprobados: float
