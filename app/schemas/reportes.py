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


# ----- REPORTES DE ESTUDIANTES -----
class ReporteEstudiantesTotalOut(BaseModel):
    total: int


class ReporteEstudiantesPorSucursalOut(BaseModel):
    sucursal_id: int
    nombre: str
    total: int


class ReporteEstudiantesPorTipoOut(BaseModel):
    tipo: str
    total: int


class ReporteEstudiantesPorGeneroOut(BaseModel):
    genero: str
    total: int


class ReporteEstudiantesPorMacroDistritoOut(BaseModel):
    macro_distrito: str
    total: int
