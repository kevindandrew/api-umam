from .base import Base
from .rol import Rol
from .year import Year
from .gestion import Gestion
from .sucursal import Sucursal
from .usuario import Usuario
from .aula import Aula
from .curso import Curso
from .curso_docente import CursoDocente
from .curso_sucursal import CursoSucursal
from .horario import Horario
from .hora import Hora
from .dia_semana import DiaSemana
from .dia_clase import DiasClase
from .estudiante import Estudiante
from .datos_familiares import DatosFamiliar
from .datos_academicos import DatosAcademico
from .datos_medicos import DatosMedico
from .matricula import Matricula

__all__ = [
    "Base",
    "Rol",
    "Year",
    "Gestion",
    "Sucursal",
    "Usuario",
    "Aula",
    "Curso",
    "CursoDocente",
    "CursoSucursal",
    "Horario",
    "Hora",
    "DiaSemana",
    "DiasClase",
    "Estudiante",
    "DatosFamiliar",
    "DatosAcademico",
    "DatosMedico",
    "Matricula",
]
