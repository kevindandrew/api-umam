from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class DatosAcademico(Base):
    __tablename__ = "datos_academicos"

    academico_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    estudiante_id: Mapped[int] = mapped_column(
        ForeignKey("estudiantes.estudiante_id"), nullable=False)

    grado_institucion: Mapped[str] = mapped_column(String(100), nullable=True)
    anios_servicio: Mapped[int] = mapped_column(Integer, nullable=True)
    ultimo_cargo: Mapped[str] = mapped_column(String(100), nullable=True)
    otras_habilidades: Mapped[str] = mapped_column(Text, nullable=True)

    # Relación inversa
    estudiante: Mapped["Estudiante"] = relationship(
        back_populates="datos_academicos")
