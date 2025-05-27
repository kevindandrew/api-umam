from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Aula(Base):
    __tablename__ = "aulas"

    aula_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_aula: Mapped[str] = mapped_column(String(50), nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey("sucursales.sucursal_id"), nullable=False)

    # Relaciones
    sucursal: Mapped["Sucursal"] = relationship(back_populates="aulas")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="aula")
