from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class DiasClase(Base):
    __tablename__ = "dias_clase"

    dia_clase_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    horario_id: Mapped[int] = mapped_column(
        ForeignKey("horarios.horario_id"), nullable=False)
    dia_semana_id: Mapped[int] = mapped_column(
        ForeignKey("dias_semana.dias_semana_id"), nullable=False)
    hora_id: Mapped[int] = mapped_column(
        ForeignKey("hora.hora_id"), nullable=False)

    # Relaciones
    horario: Mapped["Horario"] = relationship(back_populates="dias_clase")
    dia_semana: Mapped["DiaSemana"] = relationship(back_populates="dias_clase")
    hora: Mapped["Hora"] = relationship(back_populates="dias_clase")
