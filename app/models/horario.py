from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Horario(Base):
    __tablename__ = "horarios"

    horario_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.curso_id"), nullable=False)
    aula_id: Mapped[int] = mapped_column(
        ForeignKey("aulas.aula_id"), nullable=False)
    profesor_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.usuario_id"), nullable=False)
    gestion_id: Mapped[int] = mapped_column(
        ForeignKey("gestion.gestion_id"), nullable=False)

    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relaciones
    curso: Mapped["Curso"] = relationship(back_populates="horarios")
    aula: Mapped["Aula"] = relationship(back_populates="horarios")
    profesor: Mapped["Usuario"] = relationship(back_populates="horarios")
    gestion: Mapped["Gestion"] = relationship(back_populates="horarios")
    dias_clase: Mapped[list["DiasClase"]] = relationship(
        back_populates="horario")
    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="horario")
