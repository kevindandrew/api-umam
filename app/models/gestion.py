from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Gestion(Base):
    __tablename__ = "gestion"

    gestion_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    gestion: Mapped[str] = mapped_column(String(50), nullable=False)
    year_id: Mapped[int] = mapped_column(
        ForeignKey("year.year_id"), nullable=False)

    # Relación con Year
    year: Mapped["Year"] = relationship(back_populates="gestiones")

    # Relaciones con otras tablas (opcional si ya las estás usando)
    curso_docente: Mapped[list["CursoDocente"]
                          ] = relationship(back_populates="gestion")
    curso_sucursal: Mapped[list["CursoSucursal"]
                           ] = relationship(back_populates="gestion")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="gestion")
    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="gestion")
