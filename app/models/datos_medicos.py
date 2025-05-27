from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class DatosMedico(Base):
    __tablename__ = "datos_medicos"

    medico_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    estudiante_id: Mapped[int] = mapped_column(
        ForeignKey("estudiantes.estudiante_id"), nullable=False)

    sistema_salud: Mapped[str] = mapped_column(String(100), nullable=True)
    frecuencia_medico: Mapped[str] = mapped_column(String(100), nullable=True)
    enfermedad_base: Mapped[str] = mapped_column(Text, nullable=True)
    alergias: Mapped[str] = mapped_column(Text, nullable=True)
    tratamiento_especifico: Mapped[str] = mapped_column(Text, nullable=True)
    tuvo_covid: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # Relación inversa
    estudiante: Mapped["Estudiante"] = relationship(
        back_populates="datos_medicos")
