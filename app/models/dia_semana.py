from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class DiaSemana(Base):
    __tablename__ = "dias_semana"

    dias_semana_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    dia_semana: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relaciones
    dias_clase: Mapped[list["DiasClase"]] = relationship(
        back_populates="dia_semana")
