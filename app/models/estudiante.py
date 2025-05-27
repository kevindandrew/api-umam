from datetime import date, datetime
from sqlalchemy import String, Text, Date, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

    estudiante_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    ap_paterno: Mapped[str] = mapped_column(String(100), nullable=False)
    ap_materno: Mapped[str] = mapped_column(String(100), nullable=False)
    ci: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=True)
    genero: Mapped[str] = mapped_column(String(20), nullable=True)
    lugar_nacimiento: Mapped[str] = mapped_column(String(100), nullable=True)
    estado_civil: Mapped[str] = mapped_column(String(50), nullable=True)
    direccion: Mapped[str] = mapped_column(Text, nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow)
    como_se_entero: Mapped[str] = mapped_column(String(100), nullable=True)

    # Relaciones (se definirán después en los modelos correspondientes)
    datos_familiares: Mapped[list["DatosFamiliar"]
                             ] = relationship(back_populates="estudiante")
    datos_academicos: Mapped[list["DatosAcademico"]
                             ] = relationship(back_populates="estudiante")
    datos_medicos: Mapped[list["DatosMedico"]] = relationship(
        back_populates="estudiante")
    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="estudiante")
